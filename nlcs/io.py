import numpy as np
import StringIO

def csv2dict(csvtext, headers=1, delimiter=','):
    import csv
    #print csvtext
    reader = csv.reader(StringIO.StringIO(csvtext), delimiter=delimiter)
    data = {}
    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
            for head in header:
                data[head] = []
        else:
            #print len(header), len(data[1]), header
            colnum = 0
            for col in row:
                #print 'current data %-8s: %s' % (header[colnum], type(col))
                try:
                    data[header[colnum]].append(float(col))
                except:
                    data[header[colnum]].append(col)
                colnum += 1
                
        rownum += 1
    return data
