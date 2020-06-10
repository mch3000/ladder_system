import time, sys, json

def all_pairs(teams,costs,score=0.0):
    global state_level,current_state
    state_level += 1

    if len(teams) < 2:
        yield teams
        state_level += -1
        return
    t1 = teams[0]
    for i in range(1,len(teams)):
        ml = state_level+1
        if ml>=len(current_state): ml += -1
        if current_state[state_level]<i or (current_state[state_level]==i and current_state[ml]>0):
            current_state[state_level]=i
            s = costs[t1][teams[i]]
            if s+score<global_max: # and s<50.0:
                score2 = s+score
                pair = (t1,teams[i],s)
                for rest in all_pairs(teams[1:i]+teams[i+1:],costs,score2):
                    if rest==None:
                        yield None
                    else:
                        yield [pair] + rest
            else:
                yield None
            #print 'SL',state_level,current_state,len(teams)
    current_state[state_level]=1
    state_level += -1

def all_pairs_L1(teams,costs,current_pair):
    score = 0.0
    if len(teams) < 2:
        yield teams
        return
    t1 = teams[0]
    t2 = teams[current_pair]
    s = costs[t1][t2]
    if s+score<global_max: # and s<50.0:
        score2 = s+score
        pair = (t1,t2,s)
        for rest in all_pairs(teams[1:current_pair]+teams[current_pair+1:],costs,score2):
            if rest==None:
                yield None
            else:
                yield [pair] + rest
    else:
        yield None

def best_matchups(teams,costs,reset_state,best_cost,best_state):
    # badness must be list of lists
    starttime = time.time()
    
    global global_max, current_state, state_level
    global_max = best_cost+1.0
    best_score = global_max
    state_level = -1
    current_state = [1 for i in range(0,len(teams),2)]
    best_match = None
    if reset_state!=None:
        current_state = reset_state
        if best_state!=None:
            best_match = best_state
        else:
            best_match = current_state
    
    print 'CURRENT STATE'
    print len(current_state),len(teams)
    print current_state
    print '  BEST STATE SO FAR '
    print best_state
    
    match_gen = all_pairs(teams,costs)
    
    #match_gen = all_pairs_L1(teams,costs,current_pair)
    
    ct = 0
    ctn = 0
    better_found = False
    
    for match in match_gen:
        #print 'TEST',current_state,match!=None
        if match != None:
            ct+=1
            score = 0.0
            for gme in match:
                score+=gme[2]
            if score<best_score:
                best_score = score
                best_match = match
                best_state = [c for c in current_state]
                global_max = best_score
                better_found = True
        else:
            ctn+=1
        
        if ctn%1000000==0:
            if ctn>0 and ctn%1000000==0:
                print "<p>",'STATUS:',ct,ctn,best_score,round(time.time()-starttime,1),'s',"</p>"
        if ctn%10000==0 and round(time.time()-starttime)>240.0:
            print "<p>",'STATUS:',ct,ctn,best_score,round(time.time()-starttime,1),'s',"</p>"
            print "<p>",'STATUS:',best_match,'s',"</p>"
            print "<p>",'TAKING TOO LONG - JSON-EXITING',"</p>"
            return [best_state,current_state]
            break

    return [best_state,best_match]

def match_from_state(teams,costs,state):
    rteams = [t for t in teams]
    match = []
    i=0
    while True:
        if len(rteams)<2:
            break
        match.append([rteams[0],rteams[state[i]],costs[rteams[0]][rteams[state[i]]]])
        rteams = rteams[1:state[i]]+rteams[state[i]+1:]
        i+=1
    return match

    
# Load the data that PHP sent us
try:
    i=1
    best_cost = float(sys.argv[i])
    i+=1
    best_state = json.loads(sys.argv[i])
    i+=1
    current_state = json.loads(sys.argv[i])
    i+=1
    teams = json.loads(sys.argv[i])
    i+=1
    data = json.loads(sys.argv[i])
except:
    print "ERROR"
    sys.exit(1)

print 'DEBUG '
print teams
print best_state
print current_state
print best_cost

results = best_matchups(teams,data,current_state,best_cost,best_state)

print 'JSON-FOLLOWING'
print json.dumps(results)
