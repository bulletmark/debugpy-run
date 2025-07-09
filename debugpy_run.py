#!/usr/bin/python3
"""
Finds the "debugpy" package within your VSCode Python extension and then runs
it for "remote attach" debugging of the program/module you specify. If not
found in extensions, or bundled with this app, then tries to run the
global/venv installed "debugpy".
"""

# Author: Mark Blakeney, July 2020
import re
import shlex
import subprocess
import sys
from argparse import REMAINDER, ArgumentParser, Namespace
from pathlib import Path

from packaging.version import Version, parse

PROG = "debugpy"
EXTNAME = f"ms-python.{PROG}"
EXTSUBPATH = f"bundled/libs/{PROG}"
EXTOPTS = "-Xfrozen_modules=off"


def sortdir(val) -> Version:
    "Calculate a sort hash for given dir"
    ext = re.escape(EXTNAME)
    sval = re.sub(f"^.*/{ext}-", "", val.as_posix())
    sval = re.sub("[-/].*$", "", sval)
    return parse(sval)


def find_debugger(args: Namespace) -> str:
    "Return which debugger to use"
    # First look for module bundled with the extension
    if not args.no_extension:
        pdirs = list(Path("~").expanduser().glob(f".vscode*/extensions/{EXTNAME}-*"))

        # Filter out to dirs only
        if pdirs:
            pdirs = [d for d in pdirs if d.is_dir()]

        if pdirs:
            extdir = (
                sorted(pdirs, reverse=True, key=sortdir)[0]
                if len(pdirs) > 1
                else pdirs[0]
            )
            pkg = extdir / EXTSUBPATH

            if pkg.exists():
                return str(pkg)

    # Otherwise we didn't find the vscode module so use the global module
    return f"-m {PROG}"


def main():
    "Main code"
    # Process command line options
    opt = ArgumentParser(description=__doc__)
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument(
        "--listen",
        action="store_true",
        default=True,
        help="listen on given port, default=True",
    )
    grp.add_argument(
        "-C",
        "--connect",
        action="store_true",
        help="connect to given port rather than listen",
    )
    opt.add_argument(
        "-W",
        "--no-wait",
        action="store_true",
        help="do not wait on listen for client, start immediately",
    )
    opt.add_argument(
        "-p", "--port", default="5678", help="[host:]port to use, default=%(default)s"
    )
    opt.add_argument(
        "-E",
        "--no-extension",
        action="store_true",
        help=f"don't use the {PROG} bundled in the extension",
    )
    opt.add_argument(
        "-r",
        "--run-on-error",
        action="store_true",
        help="re-run program/module even on error",
    )
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument("--log-to", metavar="PATH", help="log to given path")
    grp.add_argument("--log-to-stderr", action="store_true", help="log to stderr")
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument("-m", "--module", help="python module to execute and debug")
    grp.add_argument("-c", "--code", help="python code to execute and debug")
    grp.add_argument("--pid", help="python pid to attach and debug")
    opt.add_argument(
        "-V", "--version", action="store_true", help=f"output {PROG} path and version"
    )
    opt.add_argument("program", nargs="?", help="python program to execute and debug")
    opt.add_argument("args", nargs=REMAINDER, help="remaining arguments to debug")

    # Split out special case configure arguments
    argslist = []
    cargslist = []
    takenext = False
    for arg in sys.argv[1:]:
        if takenext or arg.startswith("--configure-"):
            takenext = not takenext
            cargslist.append(arg)
        else:
            takenext = False
            argslist.append(arg)

    args = opt.parse_args(argslist)

    cmd = find_debugger(args)

    if args.version:
        res = subprocess.run(
            f"python3 {EXTOPTS} {cmd} --version".split(),
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        vers = res.stdout and res.stdout.strip()
        if vers:
            print(f"python3 {cmd} {res.stdout.strip()}")
        return

    if args.program and (args.module or args.code or args.pid):
        args.args.insert(0, args.program)
        args.program = None

    if args.program:
        if not Path(args.program).exists():
            opt.error(f"No such file: {args.program}.")
        mainargs = args.program
    elif args.module:
        mainargs = f"-m {args.module}"
    elif args.code:
        mainargs = f'-c "{args.code}"'
    elif args.pid:
        mainargs = f"--pid {args.pid}"
    else:
        opt.error("Must specify program, module, code, or pid.")

    if args.connect:
        ctype = "connect"
        wait = ""
    else:
        ctype = "listen"
        wait = "" if args.no_wait else " --wait-for-client"

    if args.log_to:
        logto = f" --log-to {args.log_to}"
    elif args.log_to_stderr:
        logto = " --log-to-stderr"
    else:
        logto = ""

    cargs = (" " + " ".join(cargslist)) if cargslist else ""

    cmdargs = f"--{ctype} {args.port}{wait}{cargs}{logto} {mainargs}"
    command = shlex.split(f"python3 {EXTOPTS} {cmd} {cmdargs}")
    if args.args:
        command.extend(args.args)

    msg = f"Running {' '.join(command)}"

    while True:
        print(msg)
        try:
            res = subprocess.run(command)
        except Exception as e:
            print(str(e), file=sys.stderr)
            break
        else:
            if not args.run_on_error and res.returncode != 0:
                break


if __name__ == "__main__":
    sys.exit(main())
