import os, sys, urllib2
from process import process
from wps.models import StreamGauge
import xml.etree.ElementTree as et

### Here is a test and example implementation of a wps process
##class test_process(process):
##    # These fields are required by the wps descriverprocess and getcapabilities
##    # requests
##    title = "Test Process"
##    abstract = "This is a test process for the sci-wps server."
##    inputs = [
##               {"identifier":"value1", #identifier for parameter, same as keyword
##                                       #for argument in execute method (below)
##                "abstract":"value1", #abstract for parameter
##                "title":"value1", #title of parameter
##                "literal":True, #is literaldata, otherwise complex
##                "datatype":"float", #datatype
##                "reference":""}, #ows:Reference or Schema to datatype
##               {"identifier":"value2",
##                "abstract":"value2",
##                "title":"value2",
##                "literal":True,
##                "datatype":"float",
##                "reference":""},
##               {"identifier":"value3",
##                "abstract":"value3",
##                "title":"value3",
##                "literal":True,
##                "datatype":"float",
##                "reference":""},
##             ]
##    outputs = [
##                {"identifier":"OUTPUT",
##                 "abstract":"Process outputs xml of mutiplication of input values.",
##                 "datatype":"text/xml",
##                 "title":"output title",
##                 "literal":False},
##              ]
##    version = "1.0"
##
##    def __init__(self):
##        # Do nothing here
##        pass
##
##    def execute(self, value1, value2, value3):
##        """
##        "execute" method is required for each wps process, this is the main
##        method that is called through the web service.
##
##        The names of the input paremeters (other than "self") are the same
##        names that will be required by the wps datainputs and should be
##        reflected in the inputs property of the class so that they appear
##        correctly in the describeprocess request.
##        """
##
##        # All wps processes are required to convert the str representation
##        # of their input parameters to the correct python type for execution
##        value1, value2, value3 = float(value1), float(value2), float(value3)
##
##        return "<float>"+str(value1 * value2 * value3)+"</float>"

class add_gauge_to_stream(process):
    # These fields are required by the wps descriverprocess and getcapabilities
    # requests
    title = "Add list of gauge ids to river segments"
    abstract = "Add relationship method for the CHISP1 Scenario #1 experiment"
    inputs = [
               {"identifier":"gauge_ids", #identifier for parameter, same as keyword
                                       #for argument in execute method (below)
                "abstract":"List of gauge ids that correspond to the SOS station ids", #abstract for parameter
                "title":"Gauge IDs", #title of parameter
                "literal":True, #is literaldata, otherwise complex
                "datatype":"list", #datatype
                "reference":""}, #ows:Reference or Schema to datatype
               {"identifier":"nhn_river_id",
                "abstract":"River segment ID in the Canadian NHN ID format",
                "title":"River Reach ID",
                "literal":True,
                "datatype":"string",
                "reference":""},
             ]
    outputs = [
                {"identifier":"Status",
                 "abstract":"Message for success or informative error message if there were problems performing the request",
                 "datatype":"text/xml",
                 "title":"Add Status",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, gauge_ids, nhn_river_id):
        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        gauge_ids = gauge_ids.split(",") # Probably a list of strings

        # Do django models here: Add
        pass

        return "Success!"

class remove_gauge_from_stream(process):
    # These fields are required by the wps descriverprocess and getcapabilities
    # requests
    title = "Remove list of gauge ids from river segments"
    abstract = "Add relationship method for the CHISP1 Scenario #1 experiment"
    inputs = [
               {"identifier":"gauge_ids", #identifier for parameter, same as keyword
                                       #for argument in execute method (below)
                "abstract":"List of gauge ids that correspond to the SOS station ids", #abstract for parameter
                "title":"Gauge IDs", #title of parameter
                "literal":True, #is literaldata, otherwise complex
                "datatype":"list", #datatype
                "reference":""}, #ows:Reference or Schema to datatype
               {"identifier":"nhn_river_id",
                "abstract":"River segment ID in the Canadian NHN ID format",
                "title":"River Reach ID",
                "literal":True,
                "datatype":"string",
                "reference":""},
             ]
    outputs = [
                {"identifier":"Status",
                 "abstract":"Message for success or informative error message if there were problems performing the request",
                 "datatype":"text/xml",
                 "title":"Add Status",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, gauge_ids, nhn_river_id):
        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        gauge_ids = gauge_ids.split(",") # Probably a list of strings

        # Do django models here: remove
        pass

        return "Success!"

class find_upstream_gauges(process):
    title = "Find and return (across CAN/US border) upstream river stream gauge ID's"
    abstract = "WPS for CHISP1 Scenario #1 that uses the http://ows.geobase.ca/wps/geobase?Service=WPS&Request=getcapabilities WPS service to determine upstream river segments and then determine the associated stream guage IDs."
    inputs = [
               {"identifier":"latitude",
                "abstract":"Latitude of point of interest in Degrees North", #abstract for parameter
                "title":"Gauge IDs", #title of parameter
                "literal":True, #is literaldata, otherwise complex
                "datatype":"float", #datatype
                "reference":""}, #ows:Reference or Schema to datatype
               {"identifier":"longitude",
                "abstract":"Longitude of point of interest in Degrees East",
                "title":"Longitude of point of interest",
                "literal":True,
                "datatype":"float",
                "reference":""},
             ]
    outputs = [
                {"identifier":"gauge_ids",
                 "abstract":"List of gauge_ids that coorespond to the upstream river segments from the point supplied",
                 "datatype":"text/xml",
                 "title":"Matching Gauge IDs",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, latitude, longitude):
        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        # http://ows.geobase.ca/wps/geobase?Service=WPS&Request=Execute&Version=1.0.0&identifier=NHNUpstreamIDs&DataInputs=latitude=49.22;longitude=-101.49
        #latitude = float(latitude)
        #longitude = float(longitude)
        upstream_request = "http://ows.geobase.ca/wps/geobase?Service=WPS&Request=Execute&Version=1.0.0&identifier=NHNUpstreamIDs&DataInputs=latitude=%s;longitude=%s" % (latitude, longitude)
        url = urllib2.urlopen(upstream_request, timeout=120)
        upstream_output = url.read()
        upstream_output = et.fromstring(upstream_output)
        upstream_segments = upstream_output.getchildren()[2].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[0]
##        upstream_segment_ids = []
        upstream_gauge_ids = []
        for i in range(1,len(upstream_segments)):
##            upstream_segment_ids.append(upstream_segments[i].getchildren()[0].getchildren()[0].text)
            for streamgauge in StreamGauge.objects.filter(river_segment_id=upstream_segments[i].getchildren()[0].getchildren()[0].text):
                upstream_gauge_ids.append(streamgauge.stream_gauge_id)
        return str(upstream_gauge_ids)

