#!/usr/bin/env python3
import json
import os
import pathlib


class Reg(object):
    """Additions registration"""
    def __init__(self):
        """..."""
        self.__reg = os.path.join(
            pathlib.Path(__file__).resolve().parent, 'static', 'reg.json')
        self.__reg_tmp = {}

    def add(self, key: str, value: any) -> None:
        """..."""
        self.__reg_tmp[key] = value
        with open(self.__reg, 'w') as registration_file:
            json.dump(self.__reg_tmp, registration_file)

    def get(self, key: str) -> any:
        """..."""
        if key not in self.__reg_tmp:
            with open(self.__reg, 'r') as registration_file:
                self.__reg_tmp = json.load(registration_file)

            if key not in self.__reg_tmp:
                return None

        return self.__reg_tmp[key]
