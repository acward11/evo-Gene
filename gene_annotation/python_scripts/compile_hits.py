#!/usr/bin/python
import sys
from Hit import Hit

class blast_filter:

    def filter(self, path, gene, name):

        hits = []
        hit_count = 0

        for line in open(path + "/" + name + ".tblastn", 'r'):

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
                    if hit.compareHits(sstart, send, sframe, query, evalue, subject) is True:
                        found = True
                        break
                if not found:
                    hits.append(Hit(subject, sstart, send, query, evalue, sframe))

        file = open(path + "/" + name + ".filtered.hits", 'w')

        for hit in hits:
            file.write(hit.hit_id + "\t" + str(hit.final_start) + "\t" + str(hit.final_end) + "\t" + str(hit.avrg_evalue) + "\n")
        file.close()

        gene.hits = hits
