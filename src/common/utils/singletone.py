#! /usr/bin/env python3


class Singleton:
    def __init__(self, _class):
        self._class = _class
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._class(*args, **kwargs)
        return self._instance
