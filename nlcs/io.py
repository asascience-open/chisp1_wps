import numpy as np

def csv2dict(csvtext, headers=1):
    import csv

    ifile  = open("temp", "w")
    ifile.write(csvtext)
    ifile.close
    ifile = open("temp", "rb")
    reader = csv.reader(ifile)
    data = {}
    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
            for head in header:
                data[head] = []
        else:
            colnum = 0
            for col in row:
                #print 'current data %-8s: %s' % (header[colnum], type(col))
                try:
                    data[header[colnum]].append(float(col))
                except:
                    data[header[colnum]].append(col)
                colnum += 1
                
        rownum += 1

    ifile.close()
    return data
