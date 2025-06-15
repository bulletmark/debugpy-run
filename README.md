## DEBUGPY-RUN
[![PyPi](https://img.shields.io/pypi/v/debugpy-run)](https://pypi.org/project/debugpy-run/)
[![AUR](https://img.shields.io/aur/version/debugpy-run)](https://aur.archlinux.org/packages/debugpy-run/)

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
it](#procedure-to-use) below.

If you have the [VS Code Python
extension](https://code.visualstudio.com/docs/languages/python)
installed then the full
[`debugpy`](https://github.com/microsoft/debugpy) debugger is already
bundled with it. You open a terminal window and run this utility to
invoke your program with arguments. The utility finds the path where
[`debugpy`](https://github.com/microsoft/debugpy) is installed and then
runs it for the program and arguments you specify, in listen mode.
Connect to it from within [VS Code](https://code.visualstudio.com/)
using the Python _Remote Attach_ debug configuration (using the default
host and port settings). You can `control+c` and then re-run the command
with changed arguments using your shell history and command line editing
facilities, for each debug run. You can also run `debugpy-run` remotely,
with `debugpy` explicitly installed for this case, to debug from [VS
Code](https://code.visualstudio.com/) to a remote machine over a
network.

This utility was developed on Arch Linux but should work on all Linux
systems where [VS Code](https://code.visualstudio.com/) is installed
with the [Python
extension](https://code.visualstudio.com/docs/languages/python). The
latest version and documentation is available at
https://github.com/bulletmark/debugpy-run.

## Installation

Arch users can install [debugpy-run from the
AUR](https://aur.archlinux.org/packages/debugpy-run/).

Python 3.6 or later is required. Also, the Python
[packaging](https://pypi.org/project/packaging/) module is required.
Note [debugpy-run is on PyPI](https://pypi.org/project/debugpy-run/) so
the easiest way to install it is to use [`uv tool`][uvtool] (or
[`pipx`][pipx] or [`pipxu`][pipxu]).

```sh
$ uv tool install debugpy-run
```

To upgrade:

```sh
$ uv tool upgrade debugpy-run
```

To uninstall:

```sh
$ uv tool uninstall debugpy-run
```

## Procedure to Use

1. Open [VS Code](https://code.visualstudio.com/) for the directory
   where your command line program is located.

2. Ensure you have added a [Debugging
   Configuration](https://code.visualstudio.com/docs/python/debugging#_initialize-configurations)
   in your `launch.json`. Specify _Remote Attach_ and just accept the
   default arguments (i.e. host = `localhost`, port = `5678`). You only
   have to do this once for each project.

3. Open a terminal (either within [VS
   Code](https://code.visualstudio.com/), or external) and type:

       $ debugpy-run my-program -- --myargs

   Now `debugpy-run` will start the `debugpy` debugger for your program,
   output a message, and then wait to be connected by [VS
   Code](https://code.visualstudio.com/).

    :warning: As seen in the above example, you should specify `--`
    after your program/module name so that debugpy-run knows where it's
    own options end, and the target options start.

    :warning: You must run `my-program` from same work directory as VS
    Code is using otherwise VS Code will not correlate your source file
    path with the code being run by debugpy. I.e. if the program is
    located at `src/my-program` with respect to the work directory then
    you must run it as `debugpy-run src/my-program -- --myargs`

4. In [VS Code](https://code.visualstudio.com/), start debugging, e.g.
   set a breakpoint then start the _Remote Attach_ debug session.

5. At any point you can `control+c` the terminal command and restart it
   with new command line arguments (e.g. using the convenience of your
   shell history and editing commands) and then restart the debug
   session in [VS Code](https://code.visualstudio.com/).

## Remote Debugging On Another Host

The `debugpy-run` utility first looks to find the `debugpy` package in
your local `~/.vscode/extensions` directory. If it fails to find that
then `debugpy-run` next tries to import `debugpy` globally. This is is
done so you can install both `debugpy-run` and `debugpy` on a remote
headless server (e.g. where [VS Code](https://code.visualstudio.com/) is
not installed) and then debug a program on that server from [VS
Code](https://code.visualstudio.com/) on your laptop/PC remotely over
the network.

So for example, I may have a program which runs on a server which want
to debug from [VS Code](https://code.visualstudio.com/) on my laptop. I
first make sure I install the necessary software on the server (you can
also do this in the programs virtual environment of course):

````
$ pipx install debugpy
$ pipx install debugpy-run
````

The start my program on the server using the debugger:
````
$ debugpy-run -p :5678 my-program -- --myargs
````

NOTE: We need to explicitly specify the `:port` for this case so that
the port is opened on the external network interface so we can connect
to it from another machine. By default, `debugpy-run`/`debugpy`
otherwise only accept local connections.

Then I go back to my laptop, ensure I have set up _Remote Attach_
debugging configured with host = `my-server` and port = `5678`, then start
debugging.

Of course, you could start `debugpy` directly yourself on the server but
the `debugpy-run` wrapper is more convenient to use and makes the usage
consistent with the familiar way you start `debugpy-run` on your
laptop/PC.

## Debugging A Program Running As Root

Another application of `debugpy-run` is that you can, as your normal
user, easily use [VS Code](https://code.visualstudio.com/) to debug a
program you run as root. E.g. run a program using `sudo`:

    $ sudo debugpy-run my-program -- --myargs

Now you can just _Remote Attach_ to it in [VS
Code](https://code.visualstudio.com/) as your normal user.

## Usage

Type `debugpy-run -h` to view the usage summary:

```
usage: debugpy-run [-h] [--listen | -C] [-W] [-p PORT] [-E] [-r]
                      [--log-to PATH | --log-to-stderr] [-m MODULE | -c CODE |
                      --pid PID] [-V]
                      [program] ...

Finds the "debugpy" package within your VSCode Python extension and then runs
it for "remote attach" debugging of the program/module you specify. If not
found in extensions, or bundled with this app, then tries to run the
global/venv installed "debugpy".

positional arguments:
  program              python program to execute and debug
  args                 remaining arguments to debug

options:
  -h, --help           show this help message and exit
  --listen             listen on given port, default=True
  -C, --connect        connect to given port rather than listen
  -W, --no-wait        do not wait on listen for client, start immediately
  -p, --port PORT      [host:]port to use, default=5678
  -E, --no-extension   don't use the debugpy bundled in the extension
  -r, --run-on-error   re-run program/module even on error
  --log-to PATH        log to given path
  --log-to-stderr      log to stderr
  -m, --module MODULE  python module to execute and debug
  -c, --code CODE      python code to execute and debug
  --pid PID            python pid to attach and debug
  -V, --version        output debugpy path and version
```

## License

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

[pipx]: https://github.com/pypa/pipx
[pipxu]: https://github.com/bulletmark/pipxu
[uvtool]: https://docs.astral.sh/uv/guides/tools/#installing-tools

<!-- vim: se ai syn=markdown: -->
