import os, sys, datetime, multiprocessing, uuid, io, usgs, gevent
from process import process
from wps.models import Server
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse
#import rpy2.robjects as robjects
from xml.dom import minidom
import numpy as np
import requests

from nlcs.models import Lake

#r = robjects.r
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))
#outputs_url = Server.objects.all()[0].implementation_site +"/outputs/"

class calc_nutrient_load(process):
    """
        For EGRET:WRTDS nutrient load calculation service will need:
        Inputs:
            Date (day) of interest
            Record of water quality measurements
            Record of stream flow measurements (need to parse as UTF-8)
                http://wqp-sos.herokuapp.com/sos?service=SOS&request=GetObservation&procedure=21IOWA-10070005&offering=21IOWA-10070005&observedProperty=Organic%20carbon
            Which Lake
    """
    title = "Nutrient load calculation service for the Great Lakes"
    abstract = "WPS for CHISP1 Scenario #2 that calculates the nutrient loading of the Great Lakes by each tributary"
    inputs = [
               {"identifier":"lake",
                "abstract":"Lake to calculate nutrient loads for", #abstract for parameter
                "title":"Lake Name", #title of parameter
                "literal":True, #is literaldata, otherwise complex
                "datatype":"string", #datatype
                "reference":""}, #ows:Reference or Schema to datatype
               {"identifier":"date",
                "abstract":"ISO representation of the date of interest",
                "title":"Date of Interest",
                "literal":True,
                "datatype":"string",
                "reference":""},
                {"identifier":"nutrient",
                "abstract":"The nutrient of interest",
                "title":"Nutrient Name",
                "literal":True,
                "datatype":"string",
                "reference":""},
             ]
    outputs = [
                {"identifier":"nlcs_output",
                 "abstract":"The various results and output from the USGS EGRET:WRTDS nutrient load model for the selected Great Lake",
                 "datatype":"text/xml",
                 "title":"Great Lakes Nutrient Load Calculation Output",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, lake, date, nutrient, **kwargs):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        def longterm(lake, date, nutrient, status_location, template, context, **kwargs):         
            ## Inputs
            if nutrient.lower() == "nitrogen":
                nutrient = "Nitrogen" # nutrient
            elif nutrient.lower() == "phosphorus":
                nutrient = "Phosphorus" # case sensitive
            lake = 'ontario' # lake
            date_range = '1979-06-10T00:00:00Z/2014-09-15T00:00:00Z' # date
            
            ## Make call to catalog get back station ids (using lake)
            tributaries = Lake.objects.get(name=lake).get_stations(nutrient, date)
            loads = []
            lats = []
            lons = []
            for tributary in tributaries:
                country = tributary.country
                gauges = tributary.streamgauge_set.all()
                maxq = 0
                if len(gauges) > 0:
                    for sg in gauges:
                        flow_request = sg.sos_endpoint
                        station = sg.station
                        if country == "US":
                            flow_args = {"request":"GetObservation", "featureID":station, "offering":"UNIT","observedProperty":"00060","beginPosition":date_range.split("/")[0]} # returns value in cfs (cubic feet per second)(00060)
                        elif country == "CAN":
                            can_flow_args = {"VERSION":"2.0", "SERVICE":"SOS", "REQUEST":"GetObservation", "featureOfInterest":station, "offering":"WATER_FLOW","observedProperty":"urn:ogc:def:phenomenon:OGC:1.0.30:waterlevel"}
                        r = requests.get(flow_request, params=flow_args)
                        raw_stream = r.text
                        wml = minidom.parseString(raw_stream)
                        if country == "US":
                            val, val_times = usgs.parse_sos_GetObservations(wml)
                        elif country == "CAN":
                            val, val_times = usgs.parse_sos_GetObservationsCAN(wms)
                        val = np.asarray(val)
                        val_times = np.asarray(val_times)
                        ## Find the nearest Q here and for each loop compare to the last to get the maxqthisQ = 
                        q = val[np.where(np.abs(date-val_times)==np.min(np.abs(date-val_times)))[0]][0]
                        if q > maxq:
                          maxq = q
                          lats.append(sg.latitude)
                          lons.append(sg.longitude)
                    conc = []
                    sample_dates = []
                    for wq in tributary.waterquality_set.all():
                        wq_request ="http://localhost:8000/sos"
                        if country == "US":
                            wq_args = {"service":"SOS", "request":"GetObservation", "version":"1.0.0", "responseformat":"text/csv", "eventtime":date_range, "offering":"network-all", "observedProperty":nutrient, "procedure":"USGS-"+wq_station}
                        elif country == "CAN":
                            wq_args = {"service":"SOS", "request":"GetObservation", "version":"1.0.0", "responseformat":"text/csv", "eventtime":date_range, "offering":"network-all", "observedProperty":nutrient, "procedure":wq_station}
                        r = requests.get(wq_request, params=wq_args)
                        wq_dict = io.csv2dict(r.text)
                        if country == "US":
                            sample_dates = sample_dates + [datetime.datetime.strptime(sample_date, "%Y-%m-%d") for sample_date in wq_dict["ActivityStartDate"]]
                            conc = conc + wq_dict["ResultMeasureValue"]
                        elif country == "CAN":
                            sample_dates = sample_dates + [datetime.datetime.strptime(sample_date, "%Y-%m-%dT%H:%M:%S") for sample_date in wq_dict["DATE"]]
                            conc = conc + wq_dict["RESULT"]
                    samplegroup = zip(sample_date, conc)
                    samplegroup.sort()
                    sample_dates, conc = zip(*samplegroup)
                    #Q = [val[np.where(np.abs(thistime-val_times)==np.min(np.abs(thistime-val_times)))[0]][0] for thistime in sample_dates] # need to ignore the closest indexes when they are outside of the period that exists for wq records...(or visa-vera)
                    sample_dates = np.asarray(sample_dates)
                    thisConc = conc[np.where(np.abs(date-sample_dates)==np.min(np.abs(date-sample_dates)))[0]]
                    loads.append(maxq * thisConc * 86400 / 0.0353147 / 1000)# load for 1 day in grams
                    #print load["US"][-1]
                
            context["progress"] = "Succeeded at " + datetime.datetime.now().__str__()
            context["done"] = True
            context["totalload"] = np.asarray(loads).sum()
            context["lake"] = lake
            context["tributaries"] = []
            for load, lat, lon in zip(loads, lats, lons):
                context["tributaries"].append({"name":"My Test Tributary", "lat":lat, "lon":lon, "load":load,"percent":load/context["totalload"]})
            context = Context(context)
            f = open(os.path.abspath(os.path.join(template_dir, "../", "outputs", status_location)), "w")
            f.write(Template(template).render(context))
            f.close()
            return template, context

        f = open(os.path.join(template_dir, 'nlcs.xml'))
        text = f.read()
        f.close()
        status = True
        progress = "Started Processing"
        done = False
        status_location = str(uuid.uuid4()) + ".xml"
        context = {#"segments":upstream_segments,
                   "status":status,
                   "title":self.title,
                   "identifier":"calc_nutrient_load",
                   "abstract":self.abstract,
                   "version":self.version,
                   "output":self.outputs[0],
                   "time":datetime.datetime.now().__str__(),
                   "progress":progress,
                   "status_location":outputs_url+status_location,
                   "done":done,
                  }
        context_dict = Context(context)
        f = open(os.path.abspath(os.path.join(template_dir, "../", "outputs", status_location)), "w")
        f.write(Template(text).render(context_dict))
        f.close()

        ##Call longterm
        
        p = multiprocessing.Process(target=longterm,
                                    args=(lake,
                                          date,
                                          nutrient,
                                          status_location,
                                          text,
                                          context_dict)
                                    )
        p.daemon = True
        p.start()
        
        #text, context = longterm(lake, date, nutrient, status_location, text, context_dict)

        return HttpResponse(Template(text).render(context_dict), content_type="text/xml")
        
