import os
import pandas as pd

MAX_SIZE = 100


def greet(name):
    return f"Hello {name}"


def calculate(x, y):
    return x + y


class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hi, {self.name}"