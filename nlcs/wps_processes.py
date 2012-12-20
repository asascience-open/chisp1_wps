import os, sys, urllib2, datetime
from process import process
from wps.models import StreamGauge
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))

class XXXXX(process):
    title = "Find and return (across CAN/US border) upstream river stream gauge IDs"
    abstract = "WPS for CHISP1 Scenario #1 that uses the http://ows.geobase.ca/wps/geobase?Service=WPS NHNUpstreamID WPS service to determine upstream river segments and then determine the associated stream guage IDs."
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
        upstream_segs = upstream_output.getchildren()[2].getchildren()[0].getchildren()[2].getchildren()[0].getchildren()[0]
        upstream_segments = []
        #print type(list(StreamGauge.objects.all())[0].river_segment_id)
        for i in range(1,len(upstream_segs)):
            upstream_segments.append({"id":upstream_segs[i].getchildren()[0].getchildren()[0].text,
                                      "gauge_ids":[],
                                      "has_gauge":False})
            filtered_sg = StreamGauge.objects.filter(river_segment_id__contains=upstream_segments[-1]["id"])
            for streamgauge in list(filtered_sg):
                upstream_segments[-1]["gauge_ids"].append(streamgauge.stream_gauge_id)
                upstream_segments[-1]["has_gauge"] = True
        f = open(os.path.join(template_dir, 'gauge_id.xml'))
        text = f.read()
        f.close()
        status = True
        context = {"segments":upstream_segments,
                   "status":status,
                   "title":self.title,
                   "identifier":"find_upstream_gauges",
                   "abstract":self.abstract,
                   "version":self.version,
                   "output":self.outputs[0],
                   "time":datetime.datetime.now().__str__(),
                  }
        context_dict = Context(context)
        return HttpResponse(Template(text).render(context_dict), content_type="text/xml")

