from xml.dom import minidom, Node
import datetime

def parse_sos_GetObservations(xml):
    timestamp = []
    value = []

    parameter_nm = str(xml.getElementsByTagName("om:observedProperty")[0].attributes["xlink:title"].value)
    units = str(xml.getElementsByTagName("wml2:uom")[0].attributes["code"].value)
    name = str(xml.getElementsByTagName("gml:name")[0].firstChild.nodeValue)

    length = xml.getElementsByTagName("wml2:value").length
    #print length
    #for i in range(0,length):
    #    print i
    #    timeText = xml.getElementsByTagName("wml2:time")[i].firstChild.nodeValue
    #    timeText = timeText[:-6]
    #    time = datetime.datetime.strptime(timeText, '%Y-%m-%dT%H:%M:%S')
    #    timestamp.append(time)
    #    value.append(float(xml.getElementsByTagName("wml2:value")[i].firstChild.nodeValue))
    value = [i.firstChild.nodeValue for i in xml.getElementsByTagName("wml2:value")]
    stime = datetime.datetime.strptime
    time = [stime(i.firstChild.nodeValue[:-6], '%Y-%m-%dT%H:%M:%S') for i in xml.getElementsByTagName("wml2:time")]
    value = map(float, value)
    return value, time
    
def parse_sos_GetObservationsCAN(xml):
    timestamp = []
    value = []

    parameter_nm = str(xml.getElementsByTagName("om:observedProperty")[0].attributes["xlink:title"].value)
    units = str(xml.getElementsByTagName("wml2:uom")[0].attributes["code"].value)
    name = str(xml.getElementsByTagName("gml:name")[0].firstChild.nodeValue)

    length = xml.getElementsByTagName("wml2:value").length
    #print length
    #for i in range(0,length):
    #    print i
    #    timeText = xml.getElementsByTagName("wml2:time")[i].firstChild.nodeValue
    #    timeText = timeText[:-6]
    #    time = datetime.datetime.strptime(timeText, '%Y-%m-%dT%H:%M:%S')
    #    timestamp.append(time)
    #    value.append(float(xml.getElementsByTagName("wml2:value")[i].firstChild.nodeValue))
    value = [i.firstChild.nodeValue for i in xml.getElementsByTagName("wml2:value")]
    stime = datetime.datetime.strptime
    time = [stime(i.firstChild.nodeValue[:-6], '%Y-%m-%dT%H:%M:%S.000Z') for i in xml.getElementsByTagName("wml2:time")]
    value = map(float, value)
    return value, time
