#!/usr/bin/env python3
import re


class StyleSheetOps(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__stylesheet = None
        self.__stylesheet_full = None
        self.__scopes = None

    def set_stylesheet(self, style_sheet: str) -> None:
        """..."""
        self.__stylesheet = self.__sanitized_stylesheet(style_sheet)
        self.__stylesheet_full = self.__stylesheet_fullscreen(
            self.__stylesheet)

    def stylesheet(self) -> str:
        """..."""
        return self.__stylesheet

    def stylesheet_fullscreen(self) -> str:
        """..."""
        return self.__stylesheet_full

    def widget_stylesheet(
            self, widget_class_name: str, propertie: str = None) -> str:
        """..."""
        if not self.__stylesheet:
            raise LookupError(
                'stylesheet: None. '
                'stylesheet was never configured. '
                'Please first use "set_stylesheet()"')
        if not self.__scopes:
            self.__scopes = self.__split_widgets_scops(self.__stylesheet)

        for scope_key, scope_value in self.__scopes.items():
            if not propertie:
                if widget_class_name == scope_key:
                    return scope_value
            else:
                if widget_class_name in scope_key and propertie in scope_key:
                    return scope_value
        return ''

    def __stylesheet_fullscreen(self, style_sheet: str) -> str:
        # ...
        stylesheet_full = style_sheet + (
            'MainWindow {'
            f'{self.widget_stylesheet("MainWindow")}'
            'border-radius: 0px;'
            'border: 0px;}')

        return stylesheet_full

    def __sanitized_stylesheet(self, style_sheet) -> str:
        """..."""
        self.__scopes = self.__split_widgets_scops(style_sheet)
        stylesheet = ''
        for scope_key, scope_value in self.__scopes.items():
            stylesheet += scope_key + ' {' + scope_value + '} '
        return stylesheet

    def __split_widgets_scops(self, stylesheet) -> dict:
        # ...
        cleanstyle = re.sub(r'(/\*.+\*/)|(^#.+$)', r'', stylesheet)

        scopes = {}
        all_scopes = cleanstyle.replace('\n', '').replace('  ', ' ').split('}')
        for scope in all_scopes:
            if '{' in scope:
                scope_keys, scope_value = scope.split('{')

                for scope_key in scope_keys.split(','):
                    scope_key = self.__clean_key(scope_key)
                    if scope_key and scope_key in scopes:
                        scope_value = self.__join_duplicate_values(
                            scope_value, scopes[scope_key])

                    scopes[scope_key] = self.__clean_value(scope_value)
        return scopes

    def __join_duplicate_values(self, new_value: str, old: str) -> str:
        # ...
        new_values = [self.__clean_value(x) for x in new_value.split(';') if x]
        old_values = [self.__clean_value(x) for x in old.split(';') if x]
        new_keys = [self.__clean_key(self.__clean_value(x).split(':')[0])
                    for x in new_value.split(';') if x]

        for old_value in old_values:
            old_key = self.__clean_key(old_value.split(':')[0])
            if old_key not in new_keys:
                new_values.insert(0, old_value)

        return ' '.join(new_values)

    @staticmethod
    def __clean_value(value: str) -> str:
        # ...
        return value.strip().strip(';').strip().replace(',', ', ').replace(
            ' ;', ';').replace(';', '; ').replace('  ', ' ').strip().replace(
            ';;', ';') + ';'

    @staticmethod
    def __clean_key(value: str) -> str:
        # ...
        return value.lstrip('#').replace(' ', '').strip()

    def __str__(self) -> str:
        return 'StyleParser'

    def __repr__(self) -> str:
        return 'StyleParser(object)'
