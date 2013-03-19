import os, sys, urllib2, datetime, multiprocessing, uuid, io, urllib2, usgs
from process import process
from wps.models import Server
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse
import rpy2.robjects as robjects
from xml.dom import minidom
import numpy as np

r = robjects.r
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
            ## Import the required R modules:
            robjects.packages.importr("EGRET") #https://github.com/USGS-CIDA/WRTDS/wiki
            robjects.packages.importr("dataRetrieval") # for the internal R data connector to get data
            try:
                #print '%s/nlcs_helper.R' % (os.path.abspath(os.path.dirname(__file__)))
                r("source('%s/nlcs_helper.R')" % os.path.abspath(os.path.dirname(__file__)))
            except:
                pass
            
            ## Inputs
            nutrient = "Nitrogen" # nutrient
            lake = 'ontario' # lake
            date_range = '1979-06-10T00:00:00Z/2014-09-15T00:00:00Z' # date
            
            ## Make call to catalog get back station ids (using lake)
            #catalog command goes here...
            tributaries = []
            stations = {}
            lats = {}
            lons = {}
            load = {}
            stations["US"] = ['01491000']
            lats["US"] = [-75]
            lons["US"] = [44]
            load["US"] = []
            stations["CAN"] = []
            for station, lat, lon in zip(stations["US"], lats["US"], lons["US"]):
                ## Call Stream Gauge sos and put response into raw_csv
                # Get volume flow data:(station, "00060", startdate, enddate)
                flow_request = "http://nwisvaws02.er.usgs.gov/ogc-swie/wml2/uv/sos?request=GetObservation&featureID=%s&offering=UNIT&observedProperty=00060&beginPosition=%s" % (station, date_range.split("/")[0]) # returns value in cfs (cubic feet per second)(00060)
                print flow_request
                url = urllib2.urlopen(flow_request, timeout=120)
                raw_stream = url.read()
                wml = minidom.parseString(raw_stream)
                val, val_times = usgs.parse_sos_GetObservations(wml)
                #add as extra col once wq data comes in
                #r('Daily = getDVData("01491000", "00060", "1979-09-01", "2011-09-30")')
                val = np.asarray(val)
                
                ## Call WQ sos and put response into raw_csv
                # Get water quality data:(station, parameter, startdate, enddate)
                #r('Sample = getSampleData("01491000", "00631", "1979-09-01", "2011-09-30")')
                #http://sos.chisp1.asascience.com/sos?service=SOS&request=GetObservation&version=1.0.0&responseformat=text/csv&eventtime=1979-06-10T00:00:00Z/2011-09-15T00:00:00Z&offering=network-all&observedProperty=Nitrogen&procedure=USGS-01491000
                wq_request ="http://sos.chisp1.asascience.com/sos?service=SOS&request=GetObservation&version=1.0.0&responseformat=text/tsv&eventtime=%s&offering=network-all&observedProperty=%s&procedure=%s" % (date_range, nutrient, "USGS-"+station)
                #url = urllib2.urlopen(wq_request, timeout=120)
                #raw_tsv = url.read()
                robjects.globalenv["tsvurl"] = wq_request
                r("Sample = process_nlcs_wq(tsvurl);")
                
                sample_dates = r("as.character(Sample$dateTime)")
                sample_dates = [datetime.datetime.strptime(sample_date, "%Y-%m-%d") for sample_date in sample_dates]
                
                #r('INFO = getMetaData("01491000", "00631", interactive=FALSE)')
                #r('Sample = mergeReport(Daily, Sample, interactive=FALSE)')
                val_times = np.asarray(val_times)
                Q = [val[np.where(np.abs(thistime-val_times)==np.min(np.abs(thistime-val_times)))[0]][0] for thistime in sample_dates] # need to ignore the closest indexes when they are outside of the period that exists for wq records...(or visa-vera)
                log_Q = list(np.log(Q))
                robjects.globalenv["Q"] = Q
                robjects.globalenv["LogQ"] = log_Q
                r('Sample <- data.frame(Sample, Q, LogQ)') #https://github.com/USGS-R/dataRetrieval/blob/master/R/mergeReport.r

                #r('multiPlotDataOverview(Sample, Daily, INFO, qUnit=1)')

                """
                # Compute annual results
                r('modelEstimation()')
                #annual_results = r.setupYears(paLong=12, paStart=1, localDaily=q_data_daily) # (paLong=12, paStart=1)
                r('AnnualResults = setupYears(paLong=12, paStart=1, localDaily=Daily)')

                r('plotConcHist(1980, 2012)')
                r('plotFluxHist(1980, 2012, fluxUnit=8)')
                r('tableResults(qUnit=1, fluxUnit=5)')
                r('tableChange(fluxUnit=5, yearPoints=c(1980, 1995, 2011))')
                r('plotFluxTimeDaily(1998, 2005)')

                r('pdf("%s_fluxtimedaily.pdf")' % os.path.abspath(os.path.join(template_dir, "../", "outputs", status_location)))
                r('plotFluxTimeDaily(2011, 2012)')
                r('dev.off()')

                #r.fluxBiasMulti(qUni=1, fluxUnit=4)
                # Mesh output of time, q, and concentration
                r('pdf("%s_plotcontours.pdf")' % os.path.abspath(os.path.join(template_dir, "../", "outputs", status_location)))
                r('plotContours(1980, 2012, 5, 1000, qUnit=1, contourLevels=seq(0,2.5, 0.25))')
                r('dev.off()')

                # Difference between years
                r('plotDiffContours(1985, 2011, 5, 1000, qUnit=1, maxDiff=1.0)')
                """
                thisQ = val[np.where(np.abs(date-val_times)==np.min(np.abs(date-val_times)))[0]][0]
                conc = r("Sample$value")
                sample_dates = np.asarray(sample_dates)
                thisConc = conc[np.where(np.abs(date-sample_dates)==np.min(np.abs(date-sample_dates)))[0]]
                load["US"].append(thisQ * thisConc * 86400 / 0.0353147 / 1000)# load for 1 day in grams
                #print load["US"][-1]
            context["progress"] = "Succeeded at " + datetime.datetime.now().__str__()
            context["done"] = True
            context["totalload"] = np.asarray(load["US"]).sum()
            context["lake"] = lake
            context["tributaries"] = [{"name":"My Test Tributary", "lat":"haha", "lon":"haha", "load":load["US"][-1],"percent":load["US"][-1]/context["totalload"]},]#tributaries
            context = Context(context)
            f = open(os.path.abspath(os.path.join(template_dir, "../", "outputs", status_location)), "w")
            f.write(Template(template).render(context))
            f.close()

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

        return HttpResponse(Template(text).render(context_dict), content_type="text/xml")
        
