import os

class ncbi_blast:


    def __init__(self, blast_path):
        self.blast_path = blast_path

    def makeblastdb(self, path, name):

        os.system(self.blast_path + "/makeblastdb -in " + path + " -dbtype nucl -out " + name + " -parse_seqids")
