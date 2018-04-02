import sys
import argparse

parser = argparse.ArgumentParser(description='Clustering Tool')

parser.add_argument("master_fasta", type=str, help='Path to master fasta file (R)')
parser.add_argument("query", type=str, help='Path to file of fasta header queries - queries assumed to be in clusters of size cluster_size (R)')
parser.add_argument("ordered_names", type=str, help="Path to text file containing the unique names of the genome in the fasta headers of the query file - number of rows in file should be = cluster_size(R)")
parser.add_argument("cluster_size", type=int, help='Cluster count (R)')
parser.add_argument("-n", type=str, help='Output name (O)', required=False, default="cluster")
parser.add_argument("-d", type=str, help='Path to output destination - requires / at end of path (O)', default="")

args = parser.parse_args()

#arguments
master_path = args.master_fasta
query_path = args.query
cluster_size = args.cluster_size
output_name = args.n #<---- fix this
output_destination = args
names_path=args.ordered_names

path_length = len(output_destination)

names = []
queries = []


#open files
file = open(query_path, 'r') #query file
file2 = open(master_path, 'r') #master fasta
file3 = open(name_path, 'r')

#getting names
for name in file3:
    names.append(name.replace("\n", '').replace("\r", ''))

#read master file
sequences = file2.readlines()

i = 0
count = 1

#get queries in list
for query in file:

    x = 0
    found = False

    #ordering clusters
    while x < len(names) and not found:
        
        if query.find(names[x]) is not -1:

            found = True #move on to next query

            # information = line.split("\t")
            if line[0] != ">":
                queries.append(">" + line.replace("\n", '').replace("\r", ''))
            else:
                queries.append(line.replace("\n", '').replace("\r", ''))


        x+=1

    if not found:
        sys.exit("Name not found in query")

#find quereies in master file - adding cluster_size sequences to file
for query in queries:

    if i == cluster_size:
        new_file.close()
        i = 0
        count += 1

    if i == 0:
        new_file = open(output_destination + output_name + "." + str(cluster_size) + "." + str(count) + ".fasta", "w+")

    found = False

    for sequence_line in lines:

        sequence_line = sequence_line.replace("\n", "").split(" ")[0]

        if len(sequence_line) > 0:

            if query == sequence_line and found is False:
                #print query + "\t" + sequence_line
                new_file.write(sequence_line + "\n")
                found = True
            elif found is True and sequence_line[0] != ">":
                new_file.write(sequence_line + "\n")

            elif found is True and sequence_line[0] is ">":
                break

    if found is True:
        i+=1
    else: print "Not found"

new_file.close()
