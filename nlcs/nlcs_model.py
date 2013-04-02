import numpy as np
import scipy.interpolate as interpolate
import sys, os, datetime, multiprocessing, io, requests, usgs, calendar
from xml.dom import minidom
from nlcs.models import Lake

timeout = 25
date_range = '1920-06-10T00:00:00Z/2014-09-15T00:00:00Z'

'''
Run the model with just the lake, parameter and date/duration as input
'''
def run(lake, parameter, date, duration):
    tribs = tribs_from_lake(lake, parameter, date)
    lake_loads = []
    latitudes = []
    longitudes = []
    for tributary in tribs: # possibly thread or multiprocess?
        country = tributary.country
        gauges = tributary.streamgauge_set.all()
        
        flow_timeseries_dicts = [get_streamflow(country, gauge.station) for gauge in gauges]
        wq_timeseries_dicts = [get_waterquality(country, wq.station, parameter) for wq in tributary.waterquality_set.all()]
        
        trib_wq_data = union(wq_timeseries_dicts)
        trib_flow_data, lat, lon = max(flow_timeseries_dicts, gauges)
        latitudes.append(lat)
        longitudes.append(lon)
        
        trib_time_data, trib_wq_data, trib_flow_data = interp(trib_wq_data, trib_flow_data, date, duration)
        trib_flux_data = compute_flux_series(trib_wq_data, trib_flow_data, country)
        lake_loads.append(compute_load(trib_flux_data))
    return lake_loads, latitudes, longitudes
        

'''
Functions to perform timeseries manipulation
'''
def interp(wq, flow, date, duration):
    wq_times = [i.toordinal() for i in wq["time"]]
    wq_vals = wq["value"]
    flow_vals = flow["value"]
    flow_times = [i.toordinal() for i in flow["time"]]
    if duration.lower() == "year":
        startdate = datetime.date(date.year, 1, 1)
        enddate = datetime.date(date.year, 12, 31)
        intrptime = np.arange(startdate, enddate+1, 1)
    elif duration.lower() == "month":
        numdays = calendar.monthrange(date.year, date.month)[1]
        startdate = datetime.date(date.year, date.month, 1).toordinal()
        enddate = datetime.date(date.year, date.month, numdays).toordinal()
        intrptime = np.arange(startdate, enddate+1, 1)
    elif duration.lower() == "day":
        intrptime = date.toordinal()
    try:
        intrpwq = interpolate.barycentric_interpolate(wq_times, wq_vals, x=intrptime)
        intrpflow = interpolate.barycentric_interpolate(flow_times, flow_vals, x=intrptime)
    except:
        print wq_times, wq_vals
        #print flow_times, flow_vals
    return intrptime, intrpwq, intrpflow
    
def compute_flux_series(wqvalues, flowvalues, country):
    #unit conversion here, both wq concentrations should be in mg/L already
    if country.lower() == "CAN":
        pass 
    elif country.lower() == "US":
        flowvalues = flowvalues / 0.00041 # convert from cfs to m^3/day
    return wqvalues * flowvalues * 0.001 / 1000 / 1000 # should end up with kg/day
    
def compute_load(flux):
    # Outputs total kg over duration
    return flux.sum() #numerical integration of flux (or just (dayvalue*day) + (dayvalue*day) ... for duration i.e. reimann sum)
    
def total_load(list_of_loads):
    return np.sum(np.asarray(list_of_loads))
    
'''
Functions to get and normalize data from heterogeneous distributed sources
'''
def get_property(parameter, country):
    if country == "CAN":
        if parameter.lower() == "nitrogen":
            parameter = "NNTKUR"
        elif parameter.lower() == "phosphorus":
            parameter = "PPUT"
    elif country == "US":
        if parameter.lower() == "nitrogen":
            parameter = "Nitrogen"
        elif parameter.lower() == "phosphorus":
            parameter = "Phosphorus"
    return parameter
            
def get_streamflow(country, stationid):
    us_flow_request = "http://webvastage6.er.usgs.gov/ogc-swie/wml2/uv/sos"
    can_flow_request = "http://ngwd-bdnes.cits.nrcan.gc.ca/GinService/sos"
    # can data have to query both live and hist
    if country == "CAN":
        flow_args = {"REQUEST":"GetObservation", 
                            "VERSION":"2.0.0", "SERVICE":"SOS", 
                            "featureOfInterest":"ca.gc.ec.station."+stationid, 
                            "offering":"WATER_FLOW",
                            "observedProperty":"urn:ogc:def:phenomenon:OGC:1.0.30:waterflow",
                        }
        sos_endpoint = can_flow_request
    elif country == "US":
        flow_args = {"request":"GetObservation", 
                        "featureID":stationid, 
                        "offering":"UNIT",
                        "observedProperty":"00060",
                        "beginPosition":date_range.split("/")[0],
                        }
        sos_endpoint = us_flow_request
    try:
        r = requests.get(sos_endpoint, params=flow_args, timeout=timeout)
        print r.url
        wml = minidom.parseString(r.text)
        if country == "CAN":
            val, val_times = usgs.parse_sos_GetObservationsCAN(wml) 
        elif country == "US":
            val, val_times = usgs.parse_sos_GetObservations(wml) 
    except:
        try:
            r = requests.get(sos_endpoint, params=flow_args, timeout=timeout)
            wml = minidom.parseString(r.text)
            if country == "CAN":
                val, val_times = usgs.parse_sos_GetObservationsCAN(wml) 
            elif country == "US":
                val, val_times = usgs.parse_sos_GetObservations(wml)
        except:
            val, val_times = None, None
    return {"value":val, "time":val_times}
    
def get_waterquality(country, stationid, parameter):
    wq_request ="http://sos.chisp1.asascience.com/sos"
    #wq_request ="http://localhost:8000/sos"
    wqsos_country_code = "network-all"
    wq_args = {"service":"SOS", 
                "request":"GetObservation", 
                "version":"1.0.0", 
                "responseFormat":"text/csv", 
                "eventtime":date_range, 
                "offering":wqsos_country_code, 
               }
    if country == "CAN":
        wq_args["procedure"] = stationid
        wq_args["responseFormat"] = "text/tsv"
        timefield = "DATE"
        timefmt = "%Y-%m-%dT%H:%M:%S"
        delimiter = '\t'
        valuefield = "RESULT"
    elif country == "US":
        wq_args["procedure"] = "USGS-"+stationid 
        delimiter = ","
        timefield = "ActivityStartDate"
        timefmt = "%Y-%m-%d"
        valuefield = "ResultMeasureValue"
    wq_args["observedProperty"] = get_property(parameter, country)
    r = requests.get(wq_request, params=wq_args, timeout=timeout)
    print r.url
    wq_dict = io.csv2dict(r.text, delimiter=delimiter)  
    sample_dates = wq_dict[timefield]
    sample_dates = [datetime.datetime.strptime(sample_date, timefmt) for sample_date in sample_dates]
    return {"time":sample_dates, "value":wq_dict[valuefield]}
    
def union(wq_dicts):
    # for tuple in list of wqdicts
    times = []
    concs = []
    times = [times+d["time"] for d in wq_dicts]
    concs = [concs+d["value"] for d in wq_dicts]
    samplegroup = zip(times, concs)
    samplegroup.sort()
    times, concs = zip(*samplegroup)
    for i,v in enumerate(concs[0]):
        if v == '':
            concs[0][i] = float('nan')
    return {"time":times[0], "value":concs[0]}
    
def max(flow_dicts, gauges):
    means = []
    for flow in flow_dicts:
        try:
            means.append(np.asarray(flow["value"]).mean())
        except:
            means.append(0)
    means = np.asarray(means)# find max at each timestep...?, also return the def. lat/lon pair for this trib
    gauges = list(gauges)
    return flow_dicts[np.where(means == means.max())[0]], gauges[np.where(means == means.max())[0]].latitude, gauges[np.where(means == means.max())[0]].longitude
        
def tribs_from_lake(lake, parameter, date):
    lake = lake.lower()
    tributaries = Lake.objects.get(name=lake).get_stations(parameter, date) #Perform database query here, possibly add time conditions here?
    return tributaries
    

    

