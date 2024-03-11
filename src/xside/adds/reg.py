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
        self.__reg_memory = {}
        self.__already_searched = {}

    def add(self, key: str, value: any) -> None:
        """..."""
        self.__reg_memory[key] = value
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
