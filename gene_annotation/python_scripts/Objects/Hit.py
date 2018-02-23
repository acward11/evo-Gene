

class Hit:

    def __init__(self, id, start, end, query, evalue):

        self.hit_id = id            #scaffold id
        self.hit_start = start      #updated start
        self.hit_end = end          #updated end

        self.avg_evalue = evalue    #average evalue of all the hits for this location

        self.hit_queries = []       #names of queries that hit this location
        self.hit_queries.append(query)


    #updates hit information if need be - returns 1 if updated, else 0
    def updateHit(self, start, end, frame, query_name, evalue):

        updated = False

        #if hit occured on the negative strand
        if int(frame) < 0:

            #flip start stop
            hold = start
            start = end
            end = hold

        #check for right overlap - updates hit_start
        if start < self.hit_start and end < self.hit_end:
            self.hit_start = start
            updated = True

        #check for left overlap - updates hit_end
        elif start > self.hit_start and end > self.hit_end :
            self.hit_end = end
            updated = True

        #check if both sides needed updated:
        elif start < self.hit_start and end > self.hit_end:
            self.hit_start = start
            self.hit_end = end

            updated = True

        if updated:
            self.hit_queries.append(query_name)
            self.avg_evalue = (self.avg_evalue + evalue)/2

            return 1
        else:
            return 0

