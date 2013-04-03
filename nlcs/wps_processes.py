import os, sys, datetime, multiprocessing, uuid, io, usgs, gevent, nlcs_model, time
from process import process
from wps.models import Server
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse
from xml.dom import minidom
import numpy as np
import requests

from nlcs.models import Lake

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))
outputs_url = Server.objects.all()[0].implementation_site +"/outputs/"

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
                {"identifier":"duration",
                "abstract":"The duration for the calculation",
                "title":"Duration to perform calculation over",
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

    def execute(self, lake, date, nutrient, duration, **kwargs):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        def longterm(lake, date, nutrient, duration, status_location, template, context, **kwargs):         
            ## Inputs
            parameter = nutrient.lower()
            lake = lake.lower() # lake
            
            ## Run Model
            t1 = time.time()
            loads, lats, lons, tribs = nlcs_model.run(lake, parameter, date, duration)
            t2 = time.time()
            print "Took %5.5f minutes" % ((t2-t1 ) / 60,)
            
            ## Write Results out to status xml
            context["progress"] = "Succeeded at " + datetime.datetime.now().__str__()
            context["done"] = True
            context["totalload"] = np.asarray(loads).sum()
            context["lake"] = lake
            context["tributaries"] = []
            for load, lat, lon, name in zip(loads, lats, lons, tribs):
                context["tributaries"].append({"name":name, "lat":lat, "lon":lon, "load":load,"percent":load/context["totalload"]})
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
                                          duration, 
                                          status_location,
                                          text,
                                          context_dict)
                                    )
        p.daemon = True
        p.start()
        
        #text, context = longterm(lake, date, nutrient, status_location, text, context_dict)

        return HttpResponse(Template(text).render(context_dict), content_type="text/xml")
        
