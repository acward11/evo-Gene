#!/usr/bin/python
import sys
from Hit import Hit

hits = []
hit_count = 0
for line in file(sys.argv[1], 'r'):
    hit_count+=1
    information = line.split("\t")

    query = information[0]         #id for query sequence
    qstart = int(information[1])   #query start
    qend = int(information[2])     #query end

    subject = information[3]       #id for hit
    sstart = int(information[4])   #hit start
    send = int(information[5])     #hit end
    sframe = int(information[6])   #hit frame
    evalue = float(information[7]) #evalue score

    #if first hit
    if len(hits) == 0:
        hits.append(Hit(subject, sstart, send, query, evalue, sframe))

    else:

        found = False

        for hit in hits:
             #if not unique hit
            if hit.compareHits(sstart, send, sframe, query, evalue):
                found = True
                break
        if not found:
            hits.append(Hit(subject, sstart, send, query, evalue, sframe))

file = open("dmc1.filtered.hits", 'w')

print str(hit_count)
print len(hits)
for hit in hits:
    file.write(hit.hit_id + "\t" + str(hit.final_start) + "\t" + str(hit.final_end) + "\t" + str(hit.avrg_evalue) + "\n")
file.close()
