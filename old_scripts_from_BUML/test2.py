import time, sys, json

def all_pairs(teams,score=0.0):
    if len(teams) < 2:
        yield teams
        return
    t1 = teams[0]
    for i in range(1,len(teams)):
        s = global_badness[t1][teams[i]]
        if s+score<global_maxscore: # and s<50.0:
            score2 = s+score
            pair = (t1,teams[i],s)
            for rest in all_pairs(teams[1:i]+teams[i+1:],score2):
                if rest==None:
                    yield None
                else:
                    yield [pair] + rest
        else:
            yield None

def best_matchups(teams,badness):
    # badness must be list of lists
    starttime = time.time()
    global global_badness
    global_badness = badness
    
    global global_maxscore
    global_maxscore = 10000.0
    
    tn = len(badness)
            
    match_gen = all_pairs(teams)
    
    best_match = None
    best_score = 10000.0
    
    
    ct = 0
    ctn = 0
    
    for match in match_gen:
        if match != None:
            ct+=1
            score = 0.0
            for gme in match:
                score+=gme[2]
            if score<best_score:
                best_score = score
                best_match = match
                global_maxscore = best_score
        else:
            ctn+=1
        
        if ctn%1000000==0:
            if ctn>0:
                print 'STATUS:',ct,ctn,best_score,round(time.time()-starttime,1),'s'

    if best_match==None:
        raise Exception('No match found')
        
    return best_match

# Load the data that PHP sent us
try:
    data = json.loads(sys.argv[1])
except:
    print "ERROR"
    sys.exit(1)
    
print type(data)
print len(data)

teams = data.keys()

print teams


