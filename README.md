dojo-skeleton
=============

Skeleton for SalzPUG’s Coding Dojos


Usage
-----

`python install.py <project_name>` will create a new directory named
*project_name* under the current directory, containing the following files:

  * `setup.cfg`: configuration file for *nosy*

  * `<project_name>.py`: write your code here

  * `test_<project_name>.py`: write the tests for your code here

Once you have made sure you have the Python packages [nose][1], [nosy][2] and
[yanc][3] installed, change to the project directory and run `nosy`.  It will
run your tests whenever you change one of the Python source files.

[1]: https://pypi.python.org/pypi/nose/
[2]: https://pypi.python.org/pypi/nosy/
[3]: https://pypi.python.org/pypi/yanc/

You can specify the following options for `install.py`:

  * `-d <directory>`, `--directory <directory>`: specify a different parent
    directory for the project directory

  * `-v`, `--virtualenv`: create a virtualenv for the project and install all
    necessary Python packages.

    If you are using *virtualenvwrapper*, the virtualenv will be installed in
    `$WORKON_HOME`.  If not, the virtualenv will be created in a directory
    named `env` inside the project directory.

**Note:** Make sure to run `install.py` with Python 2, as `nosy` is not yet
compatible with Python 3.
