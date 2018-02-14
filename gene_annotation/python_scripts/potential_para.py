#!/usr/bin/python

import sys

i = 1

#array of arrays(each array is one gene)
ids_per_gene = []
start_per_gene = []
end_per_gene = []
frame_per_gene = []

output = file("shared_hits2.out", 'w+')
output2 = file("DMC_unique.out", 'w+')

while i < len(sys.argv):

    ids = []
    start = []
    end = []
    frame = []

    for line in open(sys.argv[i], 'r'):
        line = line.replace("\n", "")
        information = line.split("\t")

        ids.append(information[0])
        start.append(information[1])
        end.append(information[2])
        frame.append(information[3])

    ids_per_gene.append(ids)
    start_per_gene.append(start)
    end_per_gene.append(end)
    frame_per_gene.append(frame)

    i+=1

x = 0
y = 0

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


               output.write(str(ids_per_gene[0][x]) + "\t" + str(final_start) + "\t" + str(final_end) + "\t" + str(frame_per_gene[0][x]) + str(frame_per_gene[1][x]) + "\n")

               found = True

       x+=1

    if found is False:
        output2.write(str(ids_per_gene[0][y]) + "\t" + str(start_per_gene[0][y]) + "\t" + str(end_per_gene[0][y]) + "\t" + str(frame_per_gene[0][y]) + "\n")

    y+=1








