#!/usr/bin/env python3
import json
import os
import pathlib

from xside.modules.platform import Platform


class Reg(object):
    """Additions registration"""
    def __init__(self, is_user_reg: bool = False):
        """..."""
        if is_user_reg:
            platform = Platform()
            if platform.operational_system() == 'windows':
                self.__path = os.path.join(
                    pathlib.Path.home(), 'AppData', 'Roaming', 'xside', 'reg')
            else:
                self.__path = os.path.join(
                    pathlib.Path.home(), '.config', 'xside', 'reg')
        else:
            self.__path = os.path.join(
                pathlib.Path(__file__).resolve().parent, 'static')

        self.__reg = os.path.join(self.__path, 'reg.json')
        self.__reg_memory = {}
        self.__already_searched = {}
        pathlib.Path(self.__path).mkdir(parents=True, exist_ok=True)

    def add(self, key: str, value: any) -> None:
        """..."""
        self.__reg_memory[key] = value

        if not os.path.isfile(self.__reg):
            with open(self.__reg, 'w') as registration_file:
                json.dump(self.__reg_memory, registration_file)
        else:
            with open(self.__reg, 'r') as registration_file:
                old_reg_memory = json.load(registration_file)
            old_reg_memory.update(self.__reg_memory)
            self.__reg_memory = old_reg_memory

            with open(self.__reg, 'w') as registration_file:
                json.dump(self.__reg_memory, registration_file)

    def get(self, key: str) -> any:
        """..."""
        if key in self.__reg_memory:
            return self.__reg_memory[key]

        if key in self.__already_searched:
            return self.__already_searched[key]

        with open(self.__reg, 'r') as registration_file:
            self.__reg_memory = json.load(registration_file)
            if key in self.__reg_memory:
                return self.__reg_memory[key]
            else:
                self.__already_searched[key] = None
                return None

    def path(self) -> str:
        """Registration path

        json db file path
        """
        return self.__path

    def set_path(self, path: str) -> None:
        """Set the registration path

        json db file path
        """
        self.__path = path
        self.__reg = os.path.join(self.__path, 'reg.json')
        pathlib.Path(self.__path).mkdir(parents=True, exist_ok=True)
