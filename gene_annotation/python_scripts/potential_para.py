#!/usr/bin/python
import sys

i = 1

#array of arrays(each array is one gene)
queries_per_gene = []
queries_start_per_gene = []
queries_end_per_gene = []

ids_per_gene = []
start_per_gene = []
end_per_gene = []
evalues_per_gene = []


output = file("shared_hits_test.out", 'w')
output2 = file("RAD51_unique.out", 'w')

while i < len(sys.argv):

    query_id = []
    query_start = []
    query_end = []

    subject_id = []
    subject_start = []
    subject_end = []
    evalue = []

    for line in open(sys.argv[i], 'r'):

        line = line.replace("\n", "")
        information = line.split("\t")

        query_id.append(information[0])
        query_start.append(information[1])
        query_end.append(information[2])

        subject_id.append(information[3])

        locations = information[4].split("-")

        subject_start.append(locations[0])
        subject_end.append(locations[1])

        evalue.append(information[5])

    queries_per_gene.append(query_id)
    queries_start_per_gene.append(query_start)
    queries_end_per_gene.append(query_end)

    ids_per_gene.append(subject_id)
    start_per_gene.append(subject_start)
    end_per_gene.append(subject_end)
    evalues_per_gene.append(evalue)

    i+=1

x = 0
y = 0


for current_gene in ids_per_gene[0]:

    found = False

    x = 0

    while x < len(ids_per_gene[1]) and found is False:

        if ids_per_gene[1][x] == current_gene:

            start1 = int(start_per_gene[0][y])
            start2 = int(start_per_gene[1][x])

            end1 = int(end_per_gene[0][y])
            end2 = int(end_per_gene[1][x])

            d1 = start1 - end2
            d2 = start2 - end1

            final_start = start1
            final_end = end2

            if (d1 < 500 and d1 > 0) or (d2 < 500 and d2 > 0):

                if d1 < 500:
                    final_start = start2
                else:
                    final_end = end2
                found = True

                #shared
                output.write(str(ids_per_gene[0][y]) + "\t" + str(final_start) + "-" + str(final_end) + "\t" + str(evalues_per_gene[0][y]) + "\n")
        x+=1

    if not found:
        output2.write(str(ids_per_gene[0][y]) + "\t" + str(start_per_gene[0][y]) + "-" + str(end_per_gene[0][y]) + "\t" + str(evalues_per_gene[0][y]) + "\n")

    y+=1










'''
for current_gene in ids_per_gene[0]:

    found = False

    x = 0

    while x < len(ids_per_gene[1]) and found is False:

       # if ids are equal
       if ids_per_gene[1][x] == current_gene:


           start1 = int(start_per_gene[0][y])
           start2 = int(start_per_gene[1][x])

           end1 = int(end_per_gene[0][y])
           end2 = int(end_per_gene[1][x])

            # if start and end positions are within 10 nucleotides of each other
           if abs(start1 - start2) <= 100 and abs(end1 - end2) <= 100:

               final_start = 1
               final_end = 1

               if start1 > start2:
                  final_start = start2
               else:
                   final_start = start1

               if end1 > end2:
                   final_end = end1
               else:
                   final_end = end2

               #shared
               output.write(queries_per_gene[0][x] + "\t" +
                            str(ids_per_gene[0][x]) + "\t" + str(final_start) + "\t" + str(final_end) + "\t" + str(evalues_per_gene[0][x]) + "\n")

               found = True

       x+=1

    if found is False:
        output2.write(str(ids_per_gene[0][y]) + "\t" + str(start_per_gene[0][y]) + "\t" + str(end_per_gene[0][y]) + "\t" + str(evalues_per_gene[0][y]) + "\n")

    y+=1

'''






