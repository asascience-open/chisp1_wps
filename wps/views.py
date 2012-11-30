import os, sys
from django.http import HttpResponse
import wps_processes
from wps_processes import *

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
        inputs = request.GET["datainputs"].lower()
    except:
        pass
    try:
        inputs = request.GET["Datainputs"].lower()
    except:
        pass
    try:
        inputs = request.GET["dataInputs"].lower()
    except:
        pass
    try:
        inputs = request.GET["DataInputs"].lower()
    except:
        pass
    try:
        inputs = request.GET["DATAINPUTS"].lower()
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
        ver = request.GET["version"].lower()
    except:
        pass
    try:
        ver = request.GET["Version"].lower()
    except:
        pass
    try:
        ver = request.GET["VERSION"].lower()
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
    ver = getVersion(request)
    if ver == "1.0.0":
        if call == 'describeprocess':
            identifier = getIdentifier(request)
            return describeProcess100(identifier)
        elif call == 'execute':
            identifier = getIdentifier(request)
            inputs = getDataInputs(request)
            return execute100(identifier, inputs)
        elif call == 'getcapabilities':
            return getCapabilities100()
    else:
        HttpResponse("Only WPS Version 1.0.0 supported")

def describeProcess100(identifier):
    processes = dir(wps_processes)
    if identifier == "all":
        for process in processes:
            try:
                constructor = globals()[process]
                process = constructor()
                process.is_wps
                #process.title
                #process.abstract
                #process.inputs
                #process.outputs
                response = str([process.title,
                              process.abstract,
                              process.inputs,
                              process.outputs]) # Replace this with template response
            except:
                pass
    else:
        for process in processes:
            if process == identifier:
                process.is_wps
                #process.title
                #process.abstract
                #process.inputs
                #process.outputs
                response = str([process.title,
                          process.abstract,
                          process.inputs,
                          process.outputs]) # Replace this with template response
    return HttpResponse(response)

def execute100(identifier, inputs):
    inputdict = {}
    inputs = inputs.strip("]").strip("[").split(";")
    for input in inputs:
        inputpair = input.split("=")
        inputdict[inputpair[0]] = inputpair[1]
    constructor = globals()[identifier]
    process = constructor()
    out = process.execute(**inputdict)
    response = str(out) # Add template reponse here
    return HttpResponse(response)

def getCapabilities100():
    return HttpResponse() # Add template response here
