#!/usr/bin/env python3
import subprocess


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
        return None
    else:
        if not stderr.decode():
            return stdout.decode().strip().strip("'").strip()
        return None
