chisp1_wps
=======
COPYRIGHT 2013 RPS ASA


This file is part of chisp1_wps.


    chisp1_wps is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.


    chisp1_wps is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.


    You should have received a copy of the GNU General Public License
    along with chisp1_wps.  If not, see <http://www.gnu.org/licenses/>.


####WPS Services for the OGC CHISP1 Interoperability Experiment

##Desciption

This is the OGC:WPS service/server for the ASA Scenario #1 and #2 components for the CHISP1 project.

##Scenario #1 Endpoints

 * [http://64.72.74.103:8080/wps/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc1]
 * [http://64.72.74.103:8080/wps/?request=GetCapabilities&version=1.0.0] [getcaps1]
 * [http://64.72.74.103:8080/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.37833023%3Blongitude=-100.78943634] [exec1]
 
 [descproc1]: http://64.72.74.103:8080/wps/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps1]: http://64.72.74.103:8080/wps/?request=GetCapabilities&version=1.0.0
 [exec1]: http://64.72.74.103:8080/wps/?request=execute&version=1.0.0&identifier=find_upstream_gauges&datainputs=latitude=49.37833023%3Blongitude=-100.78943634
 
##Scenario #2 Endpoints

 * [http://64.72.74.103:8080/nlcs/?request=DescribeProcess&identifier=all&version=1.0.0] [descproc2]
 * [http://64.72.74.103:8080/nlcs/?request=GetCapabilities&version=1.0.0] [getcaps2]
 * [http://64.72.74.103:8080/nlcs/?request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen] [exec2]
 
 [descproc2]: http://64.72.74.103:8080/nlcs/?request=DescribeProcess&identifier=all&version=1.0.0
 [getcaps2]: http://64.72.74.103:8080/nlcs/?request=GetCapabilities&version=1.0.0
 [exec2]: http://64.72.74.103:8080/nlcs/?request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen
