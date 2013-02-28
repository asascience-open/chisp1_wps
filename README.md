chisp1_wps
=======

####WPS Services for the OGC CHISP1 Interoperability Experiment

##Desciption

This is the OGC:WPS service/server for the ASA Scenario #1 and #2 components for the CHISP1 project.

##Scenario #1 Endpoints

 * [http://wps.chisp1.asascience.com/wps/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc1]
 * [http://wps.chisp1.asascience.com/wps/?request=GetCapabilities&version=1.0.0] [getcaps1]
 * [http://wps.chisp1.asascience.com/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.37833023%3Blongitude=-100.78943634] [exec1]
 
 [descproc1]: http://wps.chisp1.asascience.com/wps/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps1]: http://wps.chisp1.asascience.com/wps/?request=GetCapabilities&version=1.0.0
 [exec1]: http://wps.chisp1.asascience.com/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.37833023%3Blongitude=-100.78943634
 
##Scenario #2 Endpoints

 * [http://wps.chisp1.asascience.com/nlcs/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc2]
 * [http://wps.chisp1.asascience.com/nlcs/?request=GetCapabilities&version=1.0.0] [getcaps2]
 * [http://wps.chisp1.asascience.com/nlcs/?request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen] [exec2]
 
 [descproc2]: http://wps.chisp1.asascience.com/wps/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps2]: http://wps.chisp1.asascience.com/wps/?request=GetCapabilities&version=1.0.0
 [exec2]: http://wps.chisp1.asascience.com/nlcs/?request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen
