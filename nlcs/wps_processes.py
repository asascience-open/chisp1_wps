import os, sys, urllib2, datetime, multiprocessing, uuid, io, urllib2
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
            ## Import the required R modules:
            robjects.packages.importr("EGRET") #https://github.com/USGS-CIDA/WRTDS/wiki
            robjects.packages.importr("dataRetrieval") # for the internal R data connector to get data
            r("source('nlcs_helper.R')")
            
            ## Inputs
            nutrient = "Nitrogen" # nutrient
            lake = 'ontario' # lake
            date = '1979-06-10T00:00:00Z/2011-09-15T00:00:00Z' # date
            
            ## Make call to catalog get back station ids (using lake)
            #catalog command goes here...
            stations["US"] = ['01491000']
            stations["CAN"] = []
            for station in stations["US"]:
                ## Call Stream Gauge sos and put response into raw_csv
                # Get volume flow data:(station, "00060", startdate, enddate)
                flow_request = "http://nwisvaws02.er.usgs.gov/ogc-swie/wml2/uv/sos?request=GetObservation&featureID=%s&offering=UNIT&observedProperty=00060&beginPosition=%s" % (station, date.split("/")[0]) # returns value in cfs (cubic feet per second)(00060)
                url = urllib2.urlopen(flow_request, timeout=120)
                raw_stream = url.read()
                #parse raw_stream wml with laura's code
                #add as extra col once wq data comes in
                r('Daily = getDVData("01491000", "00060", "1979-09-01", "2011-09-30")')
                
                ## Call WQ sos and put response into raw_csv
                # Get water quality data:(station, parameter, startdate, enddate)
                #r('Sample = getSampleData("01491000", "00631", "1979-09-01", "2011-09-30")')
                #http://sos.chisp1.asascience.com/sos?service=SOS&request=GetObservation&version=1.0.0&responseformat=text/csv&eventtime=1979-06-10T00:00:00Z/2011-09-15T00:00:00Z&offering=network-all&observedProperty=Nitrogen&procedure=USGS-01491000
                wq_request ="http://sos.chisp1.asascience.com/sos?service=SOS&request=GetObservation&version=1.0.0&responseformat=text/csv&eventtime=%s&offering=network-all&observedProperty=%s&procedure=%s" % (date, nutrient, "USGS-"+station)
                url = urllib2.urlopen(wq_request, timeout=120)
                raw_csv = url.read()
                
                ## Parse csv into dict
                sos_dict = io.csv2dict(raw_csv)
                for colname in sos_dict.iterkeys():
                    robjects.globalenv[colname.replace("/", "_")] = sos_dict[colname]
                r("Sample <- process_nlcs_wq(OrganizationIdentifier,OrganizationFormalName,ActivityIdentifier,ActivityTypeCode,ActivityMediaName,ActivityMediaSubdivisionName,ActivityStartDate,ActivityStartTime_Time,ActivityStartTime_TimeZoneCode,ActivityEndDate,ActivityEndTime_Time,ActivityEndTime_TimeZoneCode,ActivityDepthHeightMeasure_MeasureValue,ActivityDepthHeightMeasure_MeasureUnitCode,ActivityDepthAltitudeReferencePointText,ActivityTopDepthHeightMeasure_MeasureValue,ActivityTopDepthHeightMeasure_MeasureUnitCode,ActivityBottomDepthHeightMeasure_MeasureValue,ActivityBottomDepthHeightMeasure_MeasureUnitCode,ProjectIdentifier,ActivityConductingOrganizationText,MonitoringLocationIdentifier,ActivityCommentText,SampleAquifer,HydrologicCondition,HydrologicEvent,SampleCollectionMethod_MethodIdentifier,SampleCollectionMethod_MethodIdentifierContext,SampleCollectionMethod_MethodName,SampleCollectionEquipmentName,ResultDetectionConditionText,CharacteristicName,ResultSampleFractionText,ResultMeasureValue,ResultMeasure_MeasureUnitCode,MeasureQualifierCode,ResultStatusIdentifier,StatisticalBaseCode,ResultValueTypeName,ResultWeightBasisText,ResultTimeBasisText,ResultTemperatureBasisText,ResultParticleSizeBasisText,PrecisionValue,ResultCommentText,USGSPCode,ResultDepthHeightMeasure_MeasureValue,ResultDepthHeightMeasure_MeasureUnitCode,ResultDepthAltitudeReferencePointText,SubjectTaxonomicName,SampleTissueAnatomyName,ResultAnalyticalMethod_MethodIdentifier,ResultAnalyticalMethod_MethodIdentifierContext,ResultAnalyticalMethod_MethodName,MethodDescriptionText,LaboratoryName,AnalysisStartDate,ResultLaboratoryCommentText,DetectionQuantitationLimitTypeName,DetectionQuantitationLimitMeasure_MeasureValue,DetectionQuantitationLimitMeasure_MeasureUnitCode,PreparationStartDate)")

                #r('INFO = getMetaData("01491000", "00631", interactive=FALSE)')
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
