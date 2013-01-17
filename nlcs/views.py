import os, sys
from django.http import HttpResponse
import wps_processes
from wps_processes import *
import django.shortcuts as dshorts
from django.template import Context, Template
from wps.models import Server

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))

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
            response.content = callback + "({data:" + response.content + "})"
        else:
            return HttpResponse(callback + "({data:" + response + "})")

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
    return HttpResponse(text, content_type="text/xml")
