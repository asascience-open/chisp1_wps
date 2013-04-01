import os, sys
from django.http import HttpResponse
import wps_processes
from wps_processes import *
import django.shortcuts as dshorts
from django.template import Context, Template
from wps.models import Server
from nlcs.models import Lake, Tributary, WaterQuality, StreamGauge

import multiprocessing, io, requests
from xml.dom import minidom

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))
timeout = 3600

def getIdentifier(request):
    try:
        ident = request.GET["identifier"].lower()
    except:
        pass
    try:
        ident = request.GET["Identifier"].lower()
    except:
        pass
    try:
        ident = request.GET["IDENTIFIER"].lower()
    except:
        pass
    return ident

def getDataInputs(request):
    try:
        inputs = request.GET["datainputs"]
    except:
        pass
    try:
        inputs = request.GET["Datainputs"]
    except:
        pass
    try:
        inputs = request.GET["dataInputs"]
    except:
        pass
    try:
        inputs = request.GET["DataInputs"]
    except:
        pass
    try:
        inputs = request.GET["DATAINPUTS"]
    except:
        pass
    return inputs

def getRequest(request):
    try:
        call = request.GET["request"].lower()
    except:
        pass
    try:
        call = request.GET["Request"].lower()
    except:
        pass
    try:
        call = request.GET["REQUEST"].lower()
    except:
        pass
    return call

def getVersion(request):
    try:
        ver = request.GET["version"]
    except:
        pass
    try:
        ver = request.GET["Version"]
    except:
        pass
    try:
        ver = request.GET["VERSION"]
    except:
        pass
    return ver

def getCallback(request):
    ver = None
    try:
        ver = request.GET["callback"]
    except:
        pass
    try:
        ver = request.GET["Callback"]
    except:
        pass
    try:
        ver = request.GET["CALLBACK"]
    except:
        pass
    return ver

def getBoundingBox(request):
    try:
        lon1,lat1,lon2,lat2,georef,other = request.GET["bboxinput"].split(",")
    except:
        pass
    try:
        lon1,lat1,lon2,lat2,georef,other = request.GET["bboxInput"].split(",")
    except:
        pass
    try:
        lon1,lat1,lon2,lat2,georef,other = request.GET["BboxInput"].split(",")
    except:
        pass
    try:
        lon1,lat1,lon2,lat2,georef,other = request.GET["BBOXINPUT"].split(",")
    except:
        pass
    return lon1,lat1,lon2,lat2,georef,other

def wps(request):
    call = getRequest(request)
    try:
        ver = getVersion(request)
    except:
        ver = "1.0.0" # Default to 1.0.0 if not supplied
    if ver == "1.0.0":
        if call == 'describeprocess':
            identifier = getIdentifier(request)
            return describeProcess100(identifier)
        elif call == 'execute':
            identifier = getIdentifier(request)
            inputs = getDataInputs(request)
            callback = getCallback(request)
            return execute100(identifier, inputs, callback)
        elif call == 'getcapabilities':
            return getCapabilities100()
    else:
        HttpResponse("Only WPS Version 1.0.0 supported")

def describeProcess100(identifier):
    processes = dir(wps_processes)
    context = {"processes":[]}
    if identifier == "all":
        for processname in processes:
            try:
                constructor = globals()[processname]
                process = constructor()
                process.is_wps
                if process.version != 0:
                    process.identifier = processname
                    context["processes"].append(process)
            except:
                pass
    else:
        for processname in processes:
            if processname == identifier:
                constructor = globals()[processname]
                process = constructor()
                process.is_wps
                context["processes"].append(process)
    f = open(os.path.join(template_dir, 'describeproc.xml'))
    text = f.read()
    f.close()
    context_dict = Context(context)
    return HttpResponse(Template(text).render(context_dict), content_type="text/xml")

def execute100(identifier, inputs, callback=None):
    inputdict = {}
    inputs = inputs.strip("]").strip("[").split(";")
    for input in inputs:
        inputpair = input.split("=")
        inputdict[inputpair[0]] = inputpair[1]
    constructor = globals()[identifier]
    process = constructor()
    out = process.execute(**inputdict)
    response = out # Render response in wps process
    if callback == None:
        if type(response) == HttpResponse:
            return response
        else:
            return HttpResponse(response)
    else:
        if type(response) == HttpResponse:
            return HttpResponse(callback + "({data:'" + response.content.replace("\n","") + "'})", content_type="text/javascript")
        else:
            return HttpResponse(callback + "({data:'" + str(response).replace("\n","") + "'})", content_type="text/javascript")

def getCapabilities100():
    processes = dir(wps_processes)
    context = {}
    context["processes"] = []
    for processname in processes:
        try:
            constructor = globals()[processname]
            process = constructor()
            process.is_wps
            if process.version != 0:
                process.identifier = processname
                context["processes"].append(process)
        except:
            pass
    context["server"] = Server.objects.values()[0]
    context["server_keywords"] = Server.objects.get().keywords.split(",")
    f = open(os.path.join(template_dir, 'getcaps.xml'))
    text = f.read()
    f.close()
    context_dict = Context(context)
    return HttpResponse(Template(text).render(context_dict), content_type="text/xml")

def outputs(request, filepath):
    f = open(os.path.abspath(os.path.join(template_dir, "../", "outputs", filepath)))
    text = f.read()
    callback = getCallback(request)
    if callback == None:
        return HttpResponse(text, content_type="text/xml")
    else:
        return HttpResponse(callback + "({data:'" + text.replace("\n","") + "'})", content_type="text/javascript")
        
def reload(request):
    #s = StreamGauge.objects.all().delete()
    #w = WaterQuality.objects.all().delete()
    #t = Tributary.objects.all().delete()
    #l = Lake.objects.all().delete()
    def longterm():
        nutrient = "Nitrogen" # nutrient
        date_range = '1920-06-10T00:00:00Z/2014-09-15T00:00:00Z' # date
        us_flow_request = "http://webvastage6.er.usgs.gov/ogc-swie/wml2/uv/sos"
        can_flow_request = "http://ngwd-bdnes.cits.nrcan.gc.ca/GinService/sos"
         # returns value in cfs (cubic feet per second)(00060)
        f = open(os.path.abspath(os.path.join(template_dir, "../", "supporting_files", 'scenario2_lake_relationships.csv')))
        csv_lines = f.readlines()
        f.close()
        #for lake in ["ontario", "erie", "huron", "michigan", "superior"]:
        #    l = Lake(name=lake)
        #    l.save()
        #for i, line in enumerate(csv_lines):
        #    if i > 0:
        #        line = line.split(",")
        #        try:
        #            t = Tributary(country=line[7].replace('"', ''), name=line[2].replace('"', ''), lake=Lake.objects.get(name=line[5].replace('"', '').lower()), has_stream=False, has_nitrogen=False, has_phosphorus=False)
        #            t.save()
        #        except:
        #            pass                
        for i, line in enumerate(csv_lines):
            if i > 377:
                line = line.split(",")
                print line[3], line[4]
                
                name = line[1].replace('"', '')
                stream_station = line[0].replace('"', '')
                wq_station = line[6].replace('"', '')
                if wq_station == '':
                    wq_station = stream_station
                tributary = Tributary.objects.get(name=line[2].replace('"', ''))
                lake = Lake.objects.get(name=line[5].replace('"', '').lower())
                country=line[7].replace('"', '')
                has_stream = line[9].replace('"', '')
                print has_stream
                if has_stream == "X":
                    has_stream = True
                else:
                    has_stream = False
                # Stream Gauge
                print country, stream_station, name, has_stream
                    
                if country == "CAN":
                    wqsos_country_code = "network-all"
                    wq_args = {"service":"SOS", "request":"GetObservation", "version":"1.0.0", "responseformat":"text/csv", "eventtime":date_range, "offering":wqsos_country_code, "observedProperty":nutrient, "procedure":wq_station}
                    if has_stream:
                        lat = float(line[3])
                        lon = float(line[4])
                        print lat, lon
                        can_flow_args = {"REQUEST":"GetObservation", "VERSION":"2.0.0", "SERVICE":"SOS", "featureOfInterest":"ca.gc.ec.station."+stream_station, "offering":"WATER_FLOW","observedProperty":"urn:ogc:def:phenomenon:OGC:1.0.30:waterflow"}
                        sos_endpoint = can_flow_request
                        r = requests.get(can_flow_request, params=can_flow_args, timeout=timeout)
                        print r.url
                        try:
                            wml = minidom.parseString(r.text)
                            val, val_times = usgs.parse_sos_GetObservationsCAN(wml)
                            #except:
                            #    can_flow_args = {"REQUEST":"GetObservation", "VERSION":"2.0.0", "SERVICE":"SOS", "featureOfInterest":"ca.gc.ec.station."+stream_station, "offering":"WATER_FLOW_LIVE","observedProperty":"urn:ogc:def:phenomenon:OGC:1.0.30:waterlevel"}
                            #    sos_endpoint = can_flow_request
                            #    r = requests.get(can_flow_request, params=can_flow_args)
                            #    wml = minidom.parseString(r.text)
                            #    val, val_times2 = usgs.parse_sos_GetObservations(wml)
                            stream_startdate = val_times[0]
                            stream_enddate = val_times[-1]
                        except:
                            pass
                elif country == "US":
                    wqsos_country_code = "network-all"
                    wq_args = {"service":"SOS", "request":"GetObservation", "version":"1.0.0", "responseformat":"text/csv", "eventtime":date_range, "offering":wqsos_country_code, "observedProperty":nutrient, "procedure":"USGS-"+wq_station}
                    if has_stream:
                        lat = float(line[3])
                        lon = float(line[4])
                        print lat, lon
                        us_flow_args = {"request":"GetObservation", "featureID":stream_station, "offering":"UNIT","observedProperty":"00060","beginPosition":date_range.split("/")[0]}
                        sos_endpoint = us_flow_request
                        r = requests.get(us_flow_request, params=us_flow_args, timeout=timeout)
                        print r.url
                        try:
                            wml = minidom.parseString(r.text)
                            val, val_times = usgs.parse_sos_GetObservations(wml)
                            stream_startdate = val_times[0]
                            stream_enddate = val_times[-1]
                        except:
                            pass
                if has_stream:
                    try:
                        s = StreamGauge(tributary=tributary, sos_endpoint=sos_endpoint, name=name, startdate=stream_startdate, enddate=stream_enddate, station=stream_station, latitude=lat, longitude=lon, )
                        s.save()
                        if tributary.has_stream != True:
                            tributary.has_stream = True
                            tributary.save()
                    except:
                        pass
                
                # WQ Station
                wq_request ="http://sos.chisp1.asascience.com/sos"
                try:
                    if country == "CAN":
                        wq_args["observedProperty"] = "NNTKUR"#"NITROGEN,TOT,KJELDAHL/UNF.REA"#"NNTKUR"
                        wq_args["responseFormat"] = "text/tsv"
                        timefield = "DATE"
                        timefmt = "%Y-%m-%dT%H:%M:%S"
                        delimiter = '\t'
                    else:
                        delimiter = ","
                        timefield = "ActivityStartDate"
                        timefmt = "%Y-%m-%d"
                    r = requests.get(wq_request, params=wq_args, timeout=timeout)
                    print r.url
                    wq_dict = io.csv2dict(r.text, delimiter=delimiter)  
                    sample_dates = wq_dict[timefield]
                    print sample_dates
                    sample_dates = [datetime.datetime.strptime(sample_date, timefmt) for sample_date in [sample_dates[0],sample_dates[-1]]]
                    wq_startdate = sample_dates[0]
                    wq_enddate = sample_dates[1]
                    w = WaterQuality(tributary=tributary, sos_endpoint=wq_request, name=name, startdate=wq_startdate, enddate=wq_enddate, station=wq_station, has_phosphorus=False, has_nitrogen=True)
                    w.save()
                    tributary.has_nitrogen = True
                    tributary.save()
                except:
                    pass
                try:
                    if country == "US":
                        wq_args["observedProperty"] = "Phosphorus"
                    else:
                        wq_args["observedProperty"] = "PPUT"#"PHOSPHORUS,UNFILTERED TOTAL" #"PPUT"
                    r = requests.get(wq_request, params=wq_args, timeout=timeout)
                    print r.url
                    wq_dict = io.csv2dict(r.text, delimiter=delimiter)
                    sample_dates = wq_dict[timefield]
                    #print sample_dates
                    sample_dates = [datetime.datetime.strptime(sample_date, timefmt) for sample_date in [sample_dates[0],sample_dates[-1]]]
                    wq_startdate = sample_dates[0]
                    wq_enddate = sample_dates[1]
                    wl = WaterQuality.objects.filter(station=wq_station)
                    if len(wl) == 0:
                        w = WaterQuality(tributary=tributary, sos_endpoint=wq_request, name=name, startdate=wq_startdate, enddate=wq_enddate, station=wq_station, has_phosphorus=True, has_nitrogen=False)
                    else:
                        w.has_phosphorus = True
                    w.save()
                    tributary.has_phosphorus = True
                    tributary.save()     
                except:
                    pass
    p = multiprocessing.Process(target=longterm)
    p.daemon = True
    p.start()
    return HttpResponse("started daemon to reload the catalog...")
                        
