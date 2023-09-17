class Group():
    def __init__(self, q):
        self.question = q
        self.count = 1
    def add(q):
        if (self.question == q) : self.count += 1

def groupUpdate(g, q):
    for gx in g:
        if gx.question == q: 
            gx.count += 1
            return
    g.append(Group(q))

def groupAppend(g, q):
    for q in g:
        if q.question == q: 
            q.count += 1
            return
    q.append(q)

def countCommon(g, c):
    cc = 0
    for q in g:
        if q.count == c: cc += 1
    return cc
    
def prntq(g):
    g_id = 0
    for q in g:
        g_id += 1
        print ("ID: ", g_id, "   Question: ", q.question, "  Count: ", q.count)

def get_questions(fname, debug = False):
    questions = []
    total_questions = 0
    total_unique_questions = 0
    groupID = 0
    num_groups = 0
    endLines = 0
    numCommon = 0
    startGroup = True
    with open(fname) as f:
        while True:
            c = f.read(1)
            if c == "\n" or not c: 
                endLines += 1
                startGroup = False
                if endLines == 2:
                    groupID += 1
                    dupEntries = countCommon(questions, num_groups)
                    if debug: prntq (questions)
                    if debug: print ("Group  ", groupID, " Num groups: ", num_groups,  
                    "  Dups: ", dupEntries)
                    total_unique_questions += dupEntries
                    total_questions += len(questions)
                    questions.clear()
                    endLines = 0
                    num_groups = 0
                    startGroup = True
                    if not c:
                        if debug: print("End of file")
                        break
                else:
                    num_groups += 1
            else:
                groupUpdate(questions, c)
                endLines = 0
    
    return [total_questions, total_unique_questions]

    
[total_questions, total_common] = get_questions('data.txt')
print ("Total questions: ", total_questions)
print ("Common questions: ", total_common)
    
