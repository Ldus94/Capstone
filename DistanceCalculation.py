import csv
import math
import arcpy
arcpy.env.overwriteOutput = True

inPath = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)
#imports input csv, creates output csv, reads csv, reads headers, adds new column for distanceKM, create constant (cons) for formula
with open (inPath, 'r') as csvinput:
  with open (outPath, 'w') as csvoutput:
    reader = csv.reader(csvinput, delimiter = ',')
    header = next(reader)
    header.append("DistanceKM")
    header.append("DistanceM")
    cons = 57.2958
    #write to output file, write headers to output file
    writer = csv.writer(csvoutput, lineterminator = '\n')
    writer.writerow(header)
    #Reads what column number lat and lon are in
    latIndex = header.index(arcpy.GetParameterAsText(2))
    lonIndex = header.index(arcpy.GetParameterAsText(3))
    latPrev = -9999
    lonPrev = -9999
    #row reads first row of variables - row is a list - first variable is stored
    for row in reader:
        lat = float(row[latIndex])
        lon = float(row[lonIndex])
        if latPrev == -9999: #if statement for previous lat
            latPrev = lat #resets lat
            lonPrev = lon #resets lon
            continue #skip
        else: #If the previous statements dont equal -9999, then append the row with the distance formula
            latPrev1 = math.sin(float(latPrev)/float(cons))
            lat1 = math.sin(float(lat)/float(cons))
            m1 = float(latPrev1)*float(lat1)
            latPrev2 = math.cos(float(latPrev)/float(cons))
            lat2 = math.cos(float(lat)/float(cons))
            m2 = float(latPrev2)*float(lat2)
            lonPrev1 = (float(lonPrev)/float(cons))
            lon1 = (float(lon)/float(cons))
            s1 = float(lonPrev1)-float(lon1)
            cos1 = math.cos(float(s1))
            m3 = float(m2)*float(cos1)
            a1 = float(m1)+float(m3)
            if a1>1:
                 a1 = 1
            acos1 = math.acos(float(a1))
            dist = 6378.8*float(acos1)
#dist = 6378.8*math.acos(math.sin(float(latPrev)/float(cons))*math.sin(lat/cons)+math.cos(latPrev/cons)*math.cos(lat/cons)*math.cos(lonPrev/cons)-(lon/cons)) #distance formula
            row.append(dist) #write formula to the DistanceKM column
            row.append(dist*1000)
            writer.writerow(row)
            latPrev = lat
            lonPrev = lon
