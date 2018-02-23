

class Hit:

    def __init__(self, id, start, end, query, evalue, frame):

        self.hit_id = id                   #scaffold id
        self.avrg_evalue = float(evalue)

        #flipping sequence
        if frame < 0:
            self.final_start = end          #updated start
            self.final_end = start          #updated end
        else:
            self.final_start = start
            self.final_end = end

        self.hits = []
        self.start_stop = []

        self.start_stop.append(start)
        self.start_stop.append(end)

        self.hits.append(self.start_stop)   #list of all hit location

        self.evalues = []
        self.evalues.append(evalue)         #average evalue of all the hits for this location

        self.hit_queries = []               #names of queries that hit this location
        self.hit_queries.append(query)


    #updates hit information if need be - returns boolean
    def compareHits(self, start, end, frame, query_name, evalue):

        updated = False

        #if hit occured on the negative strand
        if int(frame) < 0:

            #flip start stop
            hold = start
            start = end
            end = hold

        #check for left update - updates hit_start
        if start < self.final_start and end >= self.final_start and end <= self.final_end:
            self.final_start = start
            updated = True

        #check for right overlap - updates hit_end
        elif start <= self.final_end and start >= self.final_start and end > self.final_end:
            self.final_end = end
            updated = True

        #check if both sides needed updated:
        elif start < self.final_start and end > self.final_end:
            self.final_start = start
            self.final_end = end

            updated = True

        #within current hit
        elif start >= self.final_start and end <= self.final_end:
            self.avrg_evalue = (self.avrg_evalue + evalue) / 2
            self.hit_queries.append(query_name)
            self.evalues.append(evalue)

            return True

        if updated:
            self.avrg_evalue = (self.avrg_evalue + evalue)/2
            self.hit_queries.append(query_name)
            self.evalues.append(evalue)

            return True
        else:
            return False
