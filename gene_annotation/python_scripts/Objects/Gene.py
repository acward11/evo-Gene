from Hit import Hit

class Gene:

    def __init__(self, name, path_to_fasta):

        self.name = name
        self.path_to_fasta = path_to_fasta

        self.hits = []


    def addHit(self, start, end, frame, query_name, evalue):

        #add hit if no other hits were found
        if len(self.hits) is 0:
            self.hits.append(Hit(id, start, end, query_name, evalue))
            return 1

        #check for an update
        found = False
        for hit in self.hits:
            if hit.hit_id is id:
                hit.updateHit(start, end, frame, query_name, evalue)
                found = True
                break

        if found:
            return 1
        else:
            return 0