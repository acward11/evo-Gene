import os
import re
from blast import ncbi_blast

class Annotation_Configuration:

    p1 = re.compile("genome_[0-9]+")        # genome path
    p2 = re.compile("gene_[0-9]+")          # gene path

    genome_Found = False
    gene_Found = False


    def __init__(self):

        self.start_path = os.getcwd()

        self.blast = ncbi_blast
        self.hmmr_path=""
        self.job_path=""

        self.current_genome=""
        self.current_gene=""

    def createDirectory(self, variable, value):

        m1 = self.p1.match(variable)
        m2 = self.p2.match(variable)

        os.chdir(self.job_path)

        # new genome
        if m1 is not None:

            if not self.genome_Found:
                os.chdir("genomes")
                os.makedirs(variable)
                os.chdir(variable)

                self.blast.makeblastdb(value, variable)

                self.current_genome = variable
                self.genome_Found = True

            elif self.genome_Found:
                file = open("genomes/" + self.current_genome + "/README", 'w')
                file.write(value)
                file.close()

                self.genome_Found = False

        # new gene
        elif m2 is not None:

            if not self.gene_Found:
                os.chdir("genes")
                os.makedirs(variable)

                self.current_gene = variable
                self.gene_Found = True

            elif self.gene_Found:
                file = open("genes/" + self.current_gene + "/README", 'w')
                file.write(value)
                file.close()

                self.gene_Found = False

    def configure(self, file):

        configure_file = open(file, 'r')

        for line in configure_file:
            information = line.split("=")

            if len(information) > 1:
                variable = information[0]
                value = information[1].rstrip("\n")

                if variable == "PATH_TO_BLAST":
                    self.blast = ncbi_blast(value)
                elif variable == "PATH_TO_HMMR":
                    self.hmmr_path = value
                elif variable == "job_name":

                    #ask user if they want to update a job with new information
                    if os.path.exists(value):
                        print "Job already exist, do you want to update?"
                        print "Reminder - work on this function"

                    #creating new job directory
                    else:
                        self.job_path = value

                        os.makedirs(self.job_path)
                        os.chdir(self.job_path)
                        os.makedirs("genomes")
                        os.makedirs("genes")

                else:
                    self.createDirectory(variable, value)

