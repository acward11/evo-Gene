#University of Iowa - Logsdon Lab
#Author: Austin Ward
#Date: 5.9.18
import sys
import os
import argparse
import itertools

parser = argparse.ArgumentParser(description='BUSCO intersection')

parser.add_argument("-o", type=str, help='Path to output directory', default=".")
parser.add_argument("depth", type=int, help='maximum number of substitutions 1 - (# genomes) ')
parser.add_argument("total", type=int, help="total number of BUSCO genes")
parser.add_argument("config", type=str, help='path to file containing paths to BUSCO ouput files')

args = parser.parse_args()

#arguments
depth = args.depth
config = args.config
output = args.o
total = args.total

if not str(output).endswith("/"):
    output = str(output) + "/"

#returns a list of genome names and a list of list of dictonaries per genome[completed, missing, fragmented, completed + fragmented]
def read_config(config):

    header = "# Busco id	Status	Contig	Start	End	Score	Length"

    current_name = ""   #name of genome
    current_path = ""   #path to BUSCO output

    found_name = False
    found_path = False

    library = []        #list cotaining dictonaries
    names = []

    complete_dict = {}
    missing_dict = {}
    fragmented_dict = {}
    duplicated_dict = {}
    complete_frag_dict = {}

    #read busco.config file
    for config_line in open(config, "r"):

        config_line = config_line.replace("\n", "")

        try:

            if config_line.startswith("name="):
                current_name = config_line.split("=")[1]
                names.append(current_name)

                if not os.path.exists(output + current_name):
                    os.mkdir(output + current_name)

                found_name = True
            elif config_line.startswith("path="):
                current_path = config_line.split("=")[1]

                if not os.path.exists(current_path):
                    sys.exit("Path to BUSCO file doesn't exist: " + current_path)
                else:
                    found_path = True

        except IndexError:
            sys.exit("Name of data or path to file is required")

        #read in BUSCO file - sort by complete, duplicated, fragment, missing
        if found_path and found_name and config_line != "":

            current_missing = set()
            current_complete = set()
            current_fragmented = set()
            current_duplicated = set()
            current_complete_frag = set()

            #file header prep
            missing_file = open(output + current_name + "/" + current_name + "_Missing.txt", "w")
            missing_file.write(header)
            complete_file = open(output + current_name + "/" + current_name + "_Complete.txt", "w")
            complete_file.write(header)
            frag_file = open(output + current_name + "/" + current_name + "_Frag.txt", "w")
            frag_file.write(header)
            dup_file = open(output + current_name + "/" + current_name + "_Dup.txt", "w")
            dup_file.write(header)

            for busco_line in open(current_path, "r"):

                if not busco_line.startswith("#"):
                    cols = busco_line.split("\t")
                    gene = cols[0]
                    type = cols[1]

                    if type == "Missing":
                        current_missing.add(gene)
                        missing_file.write(busco_line)
                    elif type == "Complete":
                        current_complete.add(gene)
                        current_complete_frag.add(gene)
                        complete_file.write(busco_line)
                    elif type == "Fragmented":
                        current_fragmented.add(gene)
                        current_complete_frag.add(gene)
                        frag_file.write(busco_line)
                    elif type == "Duplicated":
                        current_duplicated.add(gene)
                        dup_file.write(busco_line)

            complete_dict[current_name] = current_complete
            fragmented_dict[current_name] = current_fragmented
            duplicated_dict[current_name] = current_duplicated
            missing_dict[current_name] = current_missing
            complete_frag_dict[current_name] = current_complete_frag


            found_path = False
            found_name = False

    library.append(complete_dict)
    library.append(fragmented_dict)
    library.append(duplicated_dict)
    library.append(missing_dict)
    library.append(complete_frag_dict)

    return [names,library]


#main
information = read_config(config)

names = set(information[0])
library = information[1]


name_count = len(names)

if depth > name_count or depth <= 0:
    sys.exit("Depth is out of range")

x = name_count
i = 0
difference = []
for dictonary in library:

    if i == 0:
        print "--Complete--"
    elif i == 1:
        print "--Fragmented--"
    elif i == 2:
        print "--Duplicated--"
    elif i == 3:
        print "--Missing--"
    else:
        print "--Complete + Fragmented--"
    x = name_count

    while x >= depth:

        current_names = list(itertools.combinations(names, x))

        for name in current_names:

            current_list_names = set()
            current_data = []
            j = 0
            while j < len(name):
                current_list_names.add(name[j])
                current_data.append(dictonary[name[j]])

                difference = names.difference(current_list_names)

                j += 1

            count = len(set.intersection(*current_data))

            if len(difference) == 0:
                print("ALL: %.2f" % (float(count) / float(total) * 100.))
            else:
                not_names = ""
                not_names += "Excluding "
                for exclude in difference:
                    not_names += exclude
                    not_names += " "
                not_names += " : "

                print not_names + "%.2f" % (float(count) / float(total) * 100.)
        x -= 1
    i += 1