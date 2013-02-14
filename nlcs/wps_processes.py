import os, sys, urllib2, datetime, multiprocessing, uuid
from process import process
from wps.models import Server
import xml.etree.ElementTree as et
from django.template import Context, Template
from django.http import HttpResponse
import rpy2.robjects as robjects

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
        def longterm(lake, date, nutrient, status_location, template, context, **kwargs):
            # Import the required R modules:
            #r.library("zoo") #should happen automatically
            #r.library("survival") #should happen automatically
            #r.library("plyr") #should happen automatically
            robjects.packages.importr("EGRET") #https://github.com/USGS-CIDA/WRTDS/wiki
            robjects.packages.importr("dataRetrieval") # for the internal R data connector to get data

            ##These following 2 commands rely on dataRetrieval which has an R version
            ##dependency. The project requires us to hit SOS services for this data
            ##ultimately.
            # Get water quality data:(station, parameter, startdate, enddate)
            r('Sample = getSampleData("01491000", "00631", "1979-09-01", "2011-09-30")')
            # Get volume flow data:(station, "00060", startdate, enddate)
            r('Daily = getDVData("01491000", "00060", "1979-09-01", "2011-09-30")')

            r('INFO = getMetaData("01491000", "00631", interactive=FALSE)')
            r('Sample = mergeReport(Daily, Sample, interactive=FALSE)')

            #r('multiPlotDataOverview(Sample, Daily, INFO, qUnit=1)')

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

            context["progress"] = "Succeeded at " + datetime.datetime.now().__str__()
            context["done"] = True
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
