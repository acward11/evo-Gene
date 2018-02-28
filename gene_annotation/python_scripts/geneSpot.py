import sys
import argparse

from parse_config import Annotation_Configuration
from compile_hits import blast_filter
from Genome import Genome
from blast import ncbi_blast




parser = argparse.ArgumentParser(description="Gene Spot")

parser.add_argument("config", type=str, help='Configuration File')
args = parser.parse_args()

#arguements
config_file = args.config

#variables
configuration = Annotation_Configuration()  #class for directory setup

#intializing job directory - genomes = array of Genome objects
information = configuration.configure(config_file)  #0 = genomes, 1 is blast path

genomes = information[0]
blast = information[1]

f = blast_filter()

#tblastn
for genome in genomes:
    for gene in genome.genes:
        information = blast.tblastn(genome, gene)
        f.filter(information[0], gene, information[1])