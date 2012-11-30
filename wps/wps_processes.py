import os, sys
from process import process

# Here is a test and example implementation of a wps process
class test_process(process):
    title = "Test Process"
    abstract = "This is a test process for the sci-wps server."
    inputs = ['value1',
              'value2',
              'value3',
             ]
    outputs = "Process outputs xml of mutiplication of input values."

    def __init__(self):
        pass

    def execute(value1, value2, value3):
        return value1 * value2 * value3
