#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentTypeError
import codecs
import keyword
import os
import re
import subprocess
import sys


def _decode_stdin(value):
    if sys.version_info.major < 3:
        return value.decode(sys.stdin.encoding)
    return value


_builtin_names = dir(__builtins__)


def _python_identifier(value):
    def msg(reason):
        return 'Cannot use {!r} as module name: {}'.format(value, reason)

    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', value):
        raise ArgumentTypeError(msg(
            'must start with a letter (A-Z, a-z) or underscore (_), followed '
            'by any number of letters, digits (0-9) or underscores'
        ))
    if keyword.iskeyword(value):
        raise ArgumentTypeError(msg('Python keyword'))
    if value in _builtin_names:
        raise ArgumentTypeError(msg('Python builtin name'))
    return value


def _directory_name(value):
    value = _decode_stdin(value)
    if not os.path.isdir(value):
        raise ArgumentTypeError('Directory not found: {!r}'.format(value))
    return os.path.abspath(os.path.normpath(value))


def main():
    # Setup the command line parser and parse arguments
    parser = ArgumentParser()
    parser.add_argument('project_name', type=_python_identifier)
    parser.add_argument('-d', '--directory', nargs='?', metavar='directory',
                        type=_directory_name, default='.',
                        help=('parent directory to create the project '
                              'directory in (default: current directory)'))
    parser.add_argument('-v', '--virtualenv', action='store_true',
                        help=('create a virtualenv for the project with the '
                              'required packages'))
    args = parser.parse_args()
    project_name = args.project_name

    def quit(messages):
        print(u'------------------------------------------------------------')
        print(u'Project is ready in {}'.format(target_dir))
        print(u'\n'.join(messages))
        print(u'Change to the project directory and run `nosy` to get going!')
        print(u'------------------------------------------------------------')
        sys.exit(0)

    # Create target directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(args.directory, project_name)
    os.mkdir(target_dir)

    # Copy the source files, and replace `kata` with the given project_name in
    # filenames as well as in contents
    for source in 'setup.cfg', 'kata.py', 'test_kata.py':
        source_file = os.path.join(cwd, source)
        target_filename = source.replace('kata', project_name)
        target_file = os.path.join(target_dir, target_filename)
        with codecs.open(source_file, 'r', 'utf-8') as f_in:
            with codecs.open(target_file, 'w', 'utf-8') as f_out:
                for line in f_in:
                    f_out.write(line.replace('kata', project_name))

    # Check for virtualenv
    packages = ['nose', 'nosy', 'yanc']
    package_info = 'Make sure to have {} installed.'.format(
        ', '.join('`{}`'.format(package) for package in packages)
    )

    if not args.virtualenv:
        quit([package_info])

    try:
        import virtualenv
    except ImportError:
        quit(['`virtualenv` not detected.', package_info])

    # Check for virtualenvwrapper
    workon_home = os.environ.get('WORKON_HOME')
    if workon_home:
        env_dir = os.path.join(workon_home, project_name)
        if os.path.exists(env_dir):
            quit([
                '`virtualenvwrapper` detected, but a virtualenv named {!r} '
                'already exists.',
                package_info
            ])
    # If virtualenvwrapper is not present, just create a virtualenv inside the
    # project directory
    else:
        env_dir = os.path.join(target_dir, 'env')

    # Create virtualenv and install packages
    virtualenv.create_environment(env_dir)
    pip = os.path.join(env_dir, 'bin', 'pip')
    subprocess.call([pip, 'install'] + packages)
    quit(['virtualenv created in {}'.format(env_dir)])


if __name__ == '__main__':
    main()
