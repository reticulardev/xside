#!/usr/bin/env python3
import subprocess


class Cli(object):
    """Command line utils"""

    def __init__(self):
        """Class constructor

        Initialize class attributes
        """

    @staticmethod
    def output_by_args(args: list) -> str | None:
        """output of command arguments

        by_args(['echo', '$HOME']) -> "/home/user"

        :param args: list args like: ['ls', '-l']
        """
        try:
            command = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = command.communicate()
        except ValueError as er:
            print(er)
            print(f'Error in command args: "{command_args}"')
        else:
            if not stderr.decode():
                return stdout.decode().strip().strip("'").strip()
            return None

    def __str__(self) -> str:
        return 'Cli'

    def __repr__(self) -> str:
        return 'Cli(object)'
