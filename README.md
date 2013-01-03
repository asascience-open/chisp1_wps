chisp1_wps
=======

####WPS Services for the OGC CHISP1 Interoperability Experiment

##Desciption

This is the OGC:WPS service/server for the ASA Scenario #1 and #2 components for the CHISP1 project.

##Scenario #1 Endpoints

 * [http://64.72.74.103:8080/wps/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc1]
 * [http://64.72.74.103:8080/wps/?request=GetCapabilities&version=1.0.0] [getcaps1]
 * [http://64.72.74.103:8080/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.22%3Blongitude=-101.492] [exec1]
 
 [descproc1]: http://64.72.74.103:8080/wps/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps1]: http://64.72.74.103:8080/wps/?request=GetCapabilities&version=1.0.0
 [exec1]: http://64.72.74.103:8080/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.22%3Blongitude=-101.492
 
##Scenario #1 Endpoints

 * [http://64.72.74.103:8080/nlcs/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc2]
 * [http://64.72.74.103:8080/nlcs/?request=GetCapabilities&version=1.0.0] [getcaps2]
 
 [descproc2]: http://64.72.74.103:8080/wps/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps2]: http://64.72.74.103:8080/wps/?request=GetCapabilities&version=1.0.0

