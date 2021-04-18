## DEBUGPY-RUN

This utility facilitates debugging a [Python](https://www.python.org/)
command line program using [Python
extension](https://code.visualstudio.com/docs/languages/python) in
[Visual Studio Code](https://code.visualstudio.com/).

The [Python
debugger](https://code.visualstudio.com/docs/python/debugging) in [VS
Code](https://code.visualstudio.com/) is superb. However debugging a
command line program which takes arguments is a little awkward to
invoke. The [official
instructions](https://code.visualstudio.com/docs/python/debugging#_initialize-configurations)
require you to edit the command line arguments in your `launch.json`
configuration which is cumbersome to do when you want to change
arguments for each run, particularly because the [arguments have to be
quoted within a JSON data
structure](https://code.visualstudio.com/docs/python/debugging#_args).
This [question on
stackoverflow](https://stackoverflow.com/questions/43704747/visual-studio-code-run-python-file-with-arguments)
describes the problem, but there is no adequate solution. This utility
provides a solution, follow the [procedure to use
it](http:/#procedure-to-use) below.

If you have the [VS Code Python
extension](https://code.visualstudio.com/docs/languages/python)
installed then the full
[`debugpy`](https://github.com/microsoft/debugpy) debugger is already
bundled with it. You open a terminal window and run this utility to
invoke your program with arguments. The utility finds the path where
[`debugpy`](https://github.com/microsoft/debugpy) is installed and then
runs it for program and arguments you specify, in listen mode. Connect
to it from within [VS Code](https://code.visualstudio.com/) using the
Python "Remote Attach" debug configuration (using the default host and
port settings). You can just `control+c` and then re-run the command
with changed arguments using your shell history and command line editing
facilities, for each debug run.

This utility was developed on Arch Linux but should work on all Linux
systems where [VS Code](https://code.visualstudio.com/) is installed
with the [Python
extension](https://code.visualstudio.com/docs/languages/python). The
latest version and documentation is available at
https://github.com/bulletmark/debugpy-run.

### Installation

Arch users can install [debugpy-run from the
AUR](https://aur.archlinux.org/packages/debugpy-run/).

Python 3.6 or later is required. Note [debugpy-run is on
PyPI](https://pypi.org/project/debugpy-run/) so just ensure that
`python3-pip` and `python3-wheel` are installed then type the following
to install (or upgrade):

```
$ sudo pip3 install -U debugpy-run
```

Or, to install from this source repository:

```
$ git clone http://github.com/bulletmark/debugpy-run
$ cd debugpy-run
$ sudo pip3 install .
```

### Procedure to Use

1. Open [VS Code](https://code.visualstudio.com/) for the directory
   where your command line program is located.

2. Ensure you have added a [Debugging
   Configuration](https://code.visualstudio.com/docs/python/debugging#_initialize-configurations)
   in your `launch.json`. Specify "Remote Attach" and just accept the
   default arguments (i.e. host = `localhost`, port = `5678`). You only
   have to do this once.

3. Open a terminal (either within [VS
   Code](https://code.visualstudio.com/), or external) and type:

       debugpy-run my-prog args ..

   Debugpy-run will start the `debugpy` debugger for your program,
   output a message, and then wait to be connected by [VS
   Code](https://code.visualstudio.com/).

4. In [VS Code](https://code.visualstudio.com/), start debugging, e.g.
   set a breakpoint then start the Remote Attach debug session.

5. At any point you can `control+c` the terminal command and restart it
   with new command line arguments (e.g. using the convenience of your
   shell history and editing commands) and then restart the debug
   session in [VS Code](https://code.visualstudio.com/).

### Usage
```
usage: debugpy-run [-h] [--listen | -C] [-p PORT] [-r]
                   [--log-to PATH | --log-to-stderr] [-m MODULE] [-c CODE]
                   [--pid PID] [-V]
                   [program] ...

Finds the "debugpy" program within your VSCode Python extension and then runs
it for "remote attach" debugging of the program/module you specify.

positional arguments:
  program               python program to execute and debug
  args                  remaining arguments to debug

optional arguments:
  -h, --help            show this help message and exit
  --listen              listen on given port, default=True
  -C, --connect         connect to given port rather than listen
  -p PORT, --port PORT  [host:]port to use, default=5678
  -r, --run-on-error    re-run program/module even on error
  --log-to PATH         log to given path
  --log-to-stderr       log to stderr
  -m MODULE, --module MODULE
                        python module to execute and debug
  -c CODE, --code CODE  python code to execute and debug
  --pid PID             python pid to attach and debug
  -V, --version         output debugpy path and version
```

### License

Copyright (C) 2021 Mark Blakeney. This program is distributed under the
terms of the GNU General Public License.
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License at <http://www.gnu.org/licenses/> for more details.

<!-- vim: se ai syn=markdown: -->
