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
        db_path = genome.output
        query = gene.path_to_fasta
        out_fmt = "'6 qseqid qstart qend sseqid sstart send sframe evalue'"
        gene_out = gene.output
        gene_name = gene.name

        out = gene_out + "/" + gene_name


        command = (str(self.blast_path) + "/tblastn -db " + str(db_path) + "/" + str(genome.name)
                   + " -query " + str(query) + " -evalue .000001 -outfmt " + str(out_fmt) + " -out " + str(out) + ".tblastn")

        print "Running: " + str(genome.name) + "-" + str(gene_name)
        os.system(command)

        information = []
        information.append(gene_out)
        information.append(gene_name)

        return information


    def retrieveSeq(self, db, id, start, stop):
        print "hey"