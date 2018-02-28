import Gene

class Genome:

    def __init__(self, name, path_to_assembly, path_to_output):

        self.name = name
        self.path_to_assembly = path_to_assembly
        self.output = path_to_output

        self.genes = []

    def addGene(self, gene):
        self.genes.append(gene)
