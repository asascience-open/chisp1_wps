import os, sys, urllib2, datetime
from process import process
from wps.models import StreamGauge
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse
from rpy import r

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "templates"))

class calc_nutrient_load(process):
    """
        For EGRET:WRTDS nutrient load calculation service will need:
        Inputs:
            Date (day) of interest
            Record of water quality measurements
            Record of stream flow measurements
            Which Lake
    """
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
                {"identifier":"nlcs_output",
                 "abstract":"The various results and output from the USGS EGRET:WRTDS nutrient load model for the selected Great Lake",
                 "datatype":"application/json",
                 "title":"Great Lakes Nutrient Load Calculation Output",
                 "literal":False},
              ]
    version = "1.0"

    def __init__(self):
        # Do nothing here
        pass

    def execute(self, latitude, longitude, **kwargs):
        # Import the required R modules:
        #r.library("zoo") #should happen automatically
        #r.library("survival") #should happen automatically
        #r.library("plyr") #should happen automatically
        r.library("EGRET") #https://github.com/USGS-CIDA/WRTDS/wiki
        r.library("dataRetrieval") # for the internal R data connector to get data

        ##These following 2 commands rely on dataRetrieval which has an R version
        ##dependency. The project requires us to hit SOS services for this data
        ##ultimately.
        # Get water quality data:(station, parameter, startdate, enddate)
        wq_data_sample = r.getSampleData("01491000", "00631", "1979-09-01", "2011-09-30")
        # Get volume flow data:(station, "00060", startdate, enddate)
        q_data_daily = r.getDVData("01491000", "00060", "1979-09-01", "2011-09-30")

        info = r.getMetaData("01491000", "00631", interactive=False)

        #wq_data_sample = r.mergeReport(q_data_daily, wq_data_sample, interactive=False) # data retrieval
        r.assign("INFO", info)
        r.assign("Sample", wq_data_sample)
        r.assign("Daily", q_data_daily)
        r('Sample = mergeReport(Daily, Sample, interactive=FALSE)')
        #r.multiPlotDataOverview(wq_data_sample, q_data_daily, info, qUnit=1)
        r('multiPlotDataOverview(Sample, Daily, INFO, qUnit=1)')

        # Compute annual results
        #annual_results = r.setupYears(paLong=12, paStart=1, localDaily=q_data_daily) # (paLong=12, paStart=1)
        r('annual_results = setupYears(paLong=12, paStart=1, localDaily=Daily)')

        r.plotConcHist(1980, 2012)
        r.plotFluxHist(1980, 2012, fluxUnit=8)
        r.tableResults(qUnit=1, fluxUnit=5)
        r.tableChange(fluxUnit=5, yearPoints=c(1980, 1995, 2011))
        r.plotFluxTimeDaily(1998, 2005)
        r.plotFluxTimeDaily(2012, 2011.75)
        r.fluxBiasMulti(qUni=1, fluxUnit=4)
        # Mesh output of time, q, and concentration
        r.plotContours(1980, 2012, 5, 1000, qUnit=1, contourLevels=seq(0,2.5, 0.25))
        # Difference between years
        r.plotDiffContours(1985, 2011, 5, 1000, qUnit=1, maxDiff=1.0)




        f = open(os.path.join(template_dir, 'nlcs.xml'))
        text = f.read()
        f.close()
        status = True
        context = {#"segments":upstream_segments,
                   "status":status,
                   "title":self.title,
                   "identifier":"calc_nutrient_load",
                   "abstract":self.abstract,
                   "version":self.version,
                   "outputs":self.outputs,
                   "time":datetime.datetime.now().__str__(),
                  }
        context_dict = Context(context)
        return HttpResponse(Template(text).render(context_dict), content_type="text/xml")

