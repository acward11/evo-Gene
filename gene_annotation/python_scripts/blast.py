import os
from Genome import Genome
from Gene import Gene

class ncbi_blast:

    blast_path = ""

    def __init__(self, blast_path):
        self.blast_path = blast_path

    #make genome database
    def makeblastdb(self, path, name):
        os.system(self.blast_path + "/makeblastdb -in " + path + " -dbtype nucl -out " + name + " -parse_seqids")

    #tblastn
    def tblastn(self, genome, gene):

        print "Current Genome-Gene: " + genome.name + "-" + gene.name

        db_path = genome.output
        query = gene.path_to_fasta
        out_fmt = "'6 qseqid qstart qend sseqid sstart send sframe evalue'"
        gene_out = gene.output
        gene_name = gene.name

        out = gene_out + "/" + gene_name


        command = (str(self.blast_path) + "/tblastn -db " + str(db_path) + "/" + str(genome.name)
                   + " -query " + str(query) + " -evalue .000001 -outfmt " + str(out_fmt) + " -out " + str(out) + ".tblastn")


        os.system(command)

        information = []
        information.append(gene_out)
        information.append(gene_name)

        return information

    def retrieveSeq(self, genome_path, genome_name, gene_path, gene_name):

        suffix = ".filtered.hits"

        for line in open(gene_path + "/" + gene_name + suffix, 'r'):
            information = line.split("\t")

            id = information[0]
            start = information[1]
            stop = information[2]

            range = str(start) + "-" + str(stop)

            command = self.blast_path + "/blastdbcmd -db " + str(genome_path) + "/" + genome_name + " -entry " + id + " -range " + range + " >> " + gene_path + "/" + gene_name + ".hits.fasta"
            os.system(command)

        return gene_path + "/" + gene_name + ".hits.fasta"