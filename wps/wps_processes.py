import os, sys, urllib2
from process import process
from wps.models import StreamGauge
import xml.etree.ElementTree as et
from django.template import Context, loader
from django.shortcuts import render_to_response

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
                {"identifier":"longitude",
                "abstract":"Longitude in Degrees East",
                "title":"Longitude",
                "literal":True,
                "datatype":"float",
                "reference":""},
                {"identifier":"latitude",
                "abstract":"Latitude in Degrees North",
                "title":"Latitude",
                "literal":True,
                "datatype":"float",
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

    def execute(self, gauge_ids, nhn_river_id, longitude, latitude, **kwargs):
        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        try:
            gauge_ids = gauge_ids.split(",") # Probably a list of strings
            # Do django models here: Add
            for id in gauge_ids:
                if len(StreamGauge.objects.filter(stream_gauge_id=id)) != 0:
                    StreamGauge.delete(StreamGauge.objects.filter(stream_gauge_id=id)[0])
                sg_entry = StreamGauge(stream_gauge_id=id,
                                       river_segment_id=nhn_river_id,
                                       stream_gauge_x=longitude,
                                       stream_gauge_y=latitude)
                sg_entry.save()
            return "Success!"
        except Exception:
            return 'Failure!'

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

    def execute(self, gauge_ids, nhn_river_id, **kwargs):
        # All wps processes are required to convert the str representation
        # of their input parameters to the correct python type for execution
        try:
            gauge_ids = gauge_ids.split(",") # Probably a list of strings
            # Do django models here: remove
            for id in gauge_ids:
                StreamGauge.delete(StreamGauge.objects.filter(stream_gauge_id=id)[0])
            return "Success!"
        except Exception:
            return "Failure!"

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

    def execute(self, latitude, longitude, **kwargs):
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
        upstream_gauge_ids = []
        upstream_segment_ids = []
        #print type(list(StreamGauge.objects.all())[0].river_segment_id)
        for i in range(1,len(upstream_segments)):
            upstream_segment_ids.append(upstream_segments[i].getchildren()[0].getchildren()[0].text)
            #print upstream_segment_ids[i-1]
            filtered_sg = StreamGauge.objects.filter(river_segment_id__contains=upstream_segment_ids[i-1])
            #print list(filtered_sg)
            for streamgauge in list(filtered_sg):
                upstream_gauge_ids.append(streamgauge.stream_gauge_id)
        return 'gauge ids: \n' + str(upstream_gauge_ids) + '\n' + str(upstream_segment_ids)

