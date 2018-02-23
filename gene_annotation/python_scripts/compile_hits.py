#!/usr/bin/python
import sys


#adds hit information to their respected input list
def addHit(unique_hit_ids, hit_start, hit_end, id, frame, sstart, send):

    unique_hit_ids.append(id)

    #negative frame
    if int(frame) < 0:
        hit_start.append(send)
        hit_end.append(sstart)

    #positive frame
    else:
        hit_start.append(sstart)
        hit_end.append(send)

in_file = sys.argv[1]
out_file = open(sys.argv[2], 'w')

unique_hit_ids = []
hit_start = []
hit_end = []

for line in open(in_file, 'r'):

    information = line.split("\t")

    sseqid = information[0]
    sstart = information[1]
    send = information[2]
    sframe = information[3]

    found = False
    positions = []
    current_position = 0

    for current_hit in unique_hit_ids:
        if current_hit == sseqid:
            found = True
            positions.append(current_position)

        current_position+=1

    #check if start and end positions need updated
    if found:
        updated = False
        for position in positions:
            updated = False
            #negative frame (sstart > send position)
            if int(sframe) < 0:

                #update left position
                if send < hit_start[position] and sstart > hit_start[position]:
                    hit_start[position] = send
                    updated = True

                #update right position
                if sstart > hit_end[position] and send < hit_end[position]:
                    hit_end[position] = sstart
                    updated = True

            #positive frame
            else:

                #update left position
                if sstart < hit_start[position] and send > hit_start[position]:
                    hit_start[position] = sstart
                    updated = True

                #update right position
                if send > hit_end[position] and sstart < hit_end[position]:
                    hit_end[position] = send
                    updated = True
            if updated:
                break

        #unique hit found
        if not updated:
            addHit(unique_hit_ids, hit_start, hit_end, sseqid, sframe, sstart, send)



    #unique hit found
    else:
        addHit(unique_hit_ids, hit_start, hit_end, sseqid, sframe, sstart, send)

i = 0
while i < len(unique_hit_ids):

    difference = int(hit_end[i]) - int(hit_start[i])
    out_file.write(unique_hit_ids[i] + " " + hit_start[i] + "-" + hit_end[i] + "\n")

    i+=1

out_file.close()