# This is the superclass for all implmentations of wps processes
class process(object):
    title = ""
    abstract = ""
    inputs = {}
    outputs = {}
    is_wps = True
    version = 0
    def __init__(self):
        pass

    def execute():
        pass