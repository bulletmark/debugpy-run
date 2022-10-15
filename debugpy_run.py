#!/usr/bin/python3
'''
Finds the "debugpy" package within your VSCode Python extension and then
runs it for "remote attach" debugging of the program/module you specify.
If not found in extensions then tries to run the globally installed
"debugpy".
'''
# Author: Mark Blakeney, July 2020

import sys
import argparse
import subprocess
import re
from pathlib import Path
from packaging import version


PROG = 'debugpy'
EXTNAME = 'ms-python.python'

def find_ext_debugger():
    'Find where debugger is located in extensions'
    pdirs = list(Path('~').expanduser().glob(
        f'.vscode*/extensions/{EXTNAME}-*'))

    # Filter out to dirs only
    if pdirs:
        pdirs = [d for d in pdirs if d.is_dir()]

    if not pdirs:
        return None

    def sortdir(val):
        'Calculate a sort hash for given dir'
        sval = re.sub(f'^.*/{EXTNAME}-', '', str(val))
        sval = re.sub('/.*$', '', sval)
        return version.parse(sval)

    extdir = sorted(pdirs, reverse=True, key=sortdir)[0]
    pkg = extdir / f'pythonFiles/lib/python/{PROG}'
    return str(pkg) if pkg.exists() else None

def main():
    'Main code'
    # Process command line options
    opt = argparse.ArgumentParser(description=__doc__.strip())
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('--listen', action='store_true', default=True,
            help='listen on given port, default=True')
    opt.add_argument('-W', '--no-wait', action='store_true',
            help='do not wait on listen for client, start immediately')
    grp.add_argument('-C', '--connect', action='store_true',
            help='connect to given port rather than listen')
    opt.add_argument('-p', '--port', default='5678',
            help='[host:]port to use, default=%(default)s')
    grp.add_argument('-g', '--global-only', action='store_true',
            help=f'only run the globally installed {PROG}')
    opt.add_argument('-r', '--run-on-error', action='store_true',
            help='re-run program/module even on error')
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('--log-to', metavar='PATH',
            help='log to given path')
    grp.add_argument('--log-to-stderr', action='store_true',
            help='log to stderr')
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('-m', '--module',
            help='python module to execute and debug')
    grp.add_argument('-c', '--code',
            help='python code to execute and debug')
    grp.add_argument('--pid',
            help='python pid to attach and debug')
    grp.add_argument('-V', '--version', action='store_true',
            help=f'output {PROG} path and version')
    opt.add_argument('program', nargs='?',
            help='python program to execute and debug')
    opt.add_argument('args', nargs=argparse.REMAINDER,
            help='remaining arguments to debug')

    # Split out special case configure arguments
    argslist = []
    cargslist = []
    takenext = False
    for arg in sys.argv[1:]:
        if takenext or arg.startswith('--configure-'):
            takenext = not takenext
            cargslist.append(arg)
        else:
            takenext = False
            argslist.append(arg)

    args = opt.parse_args(argslist)

    cmd = None if args.global_only else find_ext_debugger()
    if not cmd:
        # We didn't find the module within the extensions so use the
        # global module
        pkg = PROG
        cmd = f'-m {pkg}'
    else:
        pkg = cmd

    if args.version:
        res = subprocess.run(f'python3 {cmd} --version'.split(),
                universal_newlines=True, stdout=subprocess.PIPE)
        vers = res.stdout and res.stdout.strip()
        if vers:
            print(f'{pkg} {res.stdout.strip()}')
        return

    if args.program and (args.module or args.code or args.pid):
        args.args.insert(0, args.program)
        args.program = None

    if args.program:
        if not Path(args.program).exists():
            opt.error(f'No such file: {args.program}.')
        mainargs = args.program
    elif args.module:
        mainargs = f'-m {args.module}'
    elif args.code:
        mainargs = f'-c {args.module}'
    elif args.pid:
        mainargs = f'--pid {args.pid}'
    else:
        opt.error('Must specify program, module, code, or pid.')

    if args.connect:
        ctype = 'connect'
        wait = ''
    else:
        ctype = 'listen'
        wait = '' if args.no_wait else ' --wait-for-client'

    if args.log_to:
        logto = f' --log-to {args.log_to}'
    elif args.log_to_stderr:
        logto = ' --log-to-stderr'
    else:
        logto = ''

    cargs = (' ' + ' '.join(cargslist)) if cargslist else ''

    cmdargs = f'--{ctype} {args.port}{wait}{cargs}{logto} {mainargs}'
    command = f'python3 {cmd} {cmdargs}'.split()
    if args.args:
        command.extend(args.args)
        xargs = ' ' + ' '.join(args.args)
    else:
        xargs = ''

    msg = f'Running {PROG} {cmdargs}{xargs}'

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

if __name__ == '__main__':
    sys.exit(main())
