import os, sys
from process import process

# Here is a test and example implementation of a wps process
class test_process(process):
    # These fields are required by the wps descriverprocess and getcapabilities
    # requests
    title = "Test Process"
    abstract = "This is a test process for the sci-wps server."
    inputs = [
               {"identifier":"value1", #identifier for parameter, same as keyword
                                       #for argument in execute method (below)
                "abstract":"value1", #abstract for parameter
                "title":"value1", #title of parameter
                "literal":True, #is literaldata, otherwise complex
                "datatype":"float", #datatype
                "reference":""}, #ows:Reference or Schema to datatype
               {"identifier":"value2",
                "abstract":"value2",
                "title":"value2",
                "literal":True,
                "datatype":"float",
                "reference":""},
               {"identifier":"value3",
                "abstract":"value3",
                "title":"value3",
                "literal":True,
                "datatype":"float",
                "reference":""},
             ]
    outputs = [
                {"identifier":"OUTPUT",
                 "abstract":"Process outputs xml of mutiplication of input values.",
                 "datatype":"text/xml",
                 "title":"output title",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, value1, value2, value3):
        """
        "execute" method is required for each wps process, this is the main
        method that is called through the web service.

        The names of the input paremeters (other than "self") are the same
        names that will be required by the wps datainputs and should be
        reflected in the inputs property of the class so that they appear
        correctly in the describeprocess request.
        """

        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        value1, value2, value3 = float(value1), float(value2), float(value3)

        return "<float>"+str(value1 * value2 * value3)+"</float>"
