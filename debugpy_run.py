#!/usr/bin/python3
'''
Finds the "debugpy" program within your VSCode Python extension and then
runs it for "remote attach" debugging of the program/module you specify.
'''
# Author: Mark Blakeney, July 2020

import sys
import argparse
import subprocess
import re
from pathlib import Path
PROG = 'debugpy'

def main():
    'Main code'
    # Process command line options
    opt = argparse.ArgumentParser(description=__doc__.strip())
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('--listen', action='store_true', default=True,
            help='listen on given port, default=True')
    grp.add_argument('-C', '--connect', action='store_true',
            help='connect to given port rather than listen')
    opt.add_argument('-p', '--port', default='5678',
            help='[host:]port to use, default=%(default)s')
    opt.add_argument('-r', '--run-on-error', action='store_true',
            help='re-run program/module even on error')
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('--log-to', metavar='PATH',
            help='log to given path')
    grp.add_argument('--log-to-stderr', action='store_true',
            help='log to stderr')
    grp = opt.add_mutually_exclusive_group()
    grp.add_argument('program', nargs='?',
            help='python program to execute and debug')
    grp.add_argument('-m', '--module',
            help='python module to execute and debug')
    grp.add_argument('-c', '--code',
            help='python code to execute and debug')
    grp.add_argument('--pid',
            help='python pid to attach and debug')
    grp.add_argument('-V', '--version', action='store_true',
            help='output debugpy path and version')
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

    pdirs = list(Path('~').expanduser().glob(
        '.vscode*/extensions/ms-python.python-*'))

    if pdirs:
        pdirs = [d for d in pdirs if d.is_dir()]

    if not pdirs:
        return 'Can\'t locate vscode python extension dir.'

    def sortdir(val):
        'Calculate a sort hash for given dir'
        valstr = re.sub(r'^.*?([0-9])', r'\1', str(val))
        v = valstr.split('.', maxsplit=3)
        return f'{v[0]}.{int(v[1]):02}.{v[2]}'

    extdir = sorted(pdirs, reverse=True, key=sortdir)[0]
    prog = extdir / f'pythonFiles/lib/python/{PROG}'
    if not prog.exists():
        return 'Can\'t locate vscode python extension.'

    if args.version:
        res = subprocess.run(f'python3 {prog} --version'.split(),
                universal_newlines=True, stdout=subprocess.PIPE)
        print(f'{prog} {res.stdout.strip()}')
        return

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
        wait = ' --wait-for-client'

    logto = ''
    if args.log_to:
        logto = f' --log-to {args.log_to}'
    elif args.log_to_stderr:
        logto = ' --log-to-stderr'

    cargs = (' ' + ' '.join(cargslist)) if cargslist else ''

    cmdargs = f'--{ctype} {args.port}{wait}{cargs}{logto} {mainargs}'
    cmd = f'python3 {prog} {cmdargs}'.split()
    if args.args:
        cmd.extend(args.args)
        xargs = ' ' + ' '.join(args.args)
    else:
        xargs = ''

    msg = f'Running {PROG} {cmdargs}{xargs}'

    while True:
        print(msg)
        try:
            res = subprocess.run(cmd)
        except KeyboardInterrupt:
            break
        if not args.run_on_error and res.returncode != 0:
            break

if __name__ == '__main__':
    sys.exit(main())
