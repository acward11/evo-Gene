import os
import re
import copy

from blast import ncbi_blast
from Genome import Genome
from Gene import Gene

class Annotation_Configuration:

    p1 = re.compile("genome_[0-9]+")        # genome path
    p2 = re.compile("gene_[0-9]+")          # gene path

    genome_Found = False
    gene_Found = False


    genomes = []

    def __init__(self):

        self.start_path = os.getcwd()

        self.blast = ncbi_blast
        self.hmmr_path=""
        self.job_path=""

        self.current_genome=""
        self.current_genome_path=""

        self.current_gene=""
        self.current_gene_path=""

    def createDirectory(self, variable, value):

        m1 = self.p1.match(variable)
        m2 = self.p2.match(variable)

        os.chdir(self.job_path)

        # new genome
        if m1 is not None:

            if not self.genome_Found:
                os.chdir("genomes")
                os.makedirs(variable)
                os.mkdir(variable + "/genes")
                os.chdir(variable)

                self.current_genome = variable
                self.current_genome_path = value
                self.genome_Found = True

            #create Genome object
            elif self.genome_Found:
                os.chdir("genomes/" + self.current_genome)

                #create genome object
                self.genomes.append(Genome(value, self.current_genome_path, os.getcwd()))

                # create blast database
                self.blast.makeblastdb(self.current_genome_path, value)

                file = open("README", 'w')
                file.write(value)
                file.close()

                self.genome_Found = False

        # new gene
        elif m2 is not None:

            if not self.gene_Found:

                self.current_gene = variable
                self.current_gene_path = value
                self.gene_Found = True

            #creating Gene object
            elif self.gene_Found:

                genes = []

                i = 0
                #creating directories and adding gene object to each genome
                while i < len(self.genomes):
                    output_path = "genomes/genome_"+ str(i + 1) + "/genes/" + self.current_gene
                    os.makedirs(output_path)

                    file = open(output_path + "/README", 'w')
                    file.write(value)
                    file.close()

                    genes.append(Gene(value, self.current_gene_path, os.getcwd() + "/" + output_path))

                    i+=1

                for genome in self.genomes:
                    for gene in genes:
                        genome.addGene(gene)

                os.chdir(self.job_path)
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

                else:
                    self.createDirectory(variable, value)

        information = []
        information.append(self.genomes)
        information.append(self.blast)

        return information
