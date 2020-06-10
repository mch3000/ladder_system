#!/usr/bin/python3

import time
import sys

# Function that searches for set of pairings with lowest total cost
# ** NOTE ** this is recursive!
# ** NOTE ** the 'yield' command is tricky - later calls to this function will return to this spot!
# Inputs:
# teams - list of teams that haven't been paired yet - initially len n, but gets shorter
# costs - list of len n of list of len n (n x n marix of costs)
# score - total score so far
#
# Global variables:
# state_level - the "level" of the tree search. top level is 0, should go to n/2
# current_state - ??
#
# Function variables:
# ta - team number of first team in list - try to pair with every other team
# ml - ??
# s - cost of current pair match
# score2 - update this with score of current pair

def all_pairs(teams,costs,score=0.0):
    global state_level,current_state
    
    # go 'down' the tree search one level:
    state_level += 1
    print('Calling all_pairs, new state_level: ',state_level)

    # if there aren't enough teams left to pair off, go back up
    if len(teams) < 2:
        yield teams
        state_level += -1
        return
    
    # try to pair off first team in list:
    ta = teams[0]
    
    # for every other team in team list:
    for i in range(1,len(teams)):
        # state level ?????
        ml = state_level+1
        
        # if ml>= ??????
        if ml>=len(current_state): ml += -1
        
        # checks that ???????
        if current_state[state_level]<i or (current_state[state_level]==i and current_state[ml]>0):
            current_state[state_level]=i
            
            # cost of current pairing
            s = costs[ta][teams[i]]
            print('Next pair: ',ta,teams[i],s)
            
            # if total cost so far is less than global_max, keep going (otherwise no point in continuing)
            if s+score<global_max: # and s<50.0:
                # update score2 with total score so far
                score2 = s+score
                
                # record this pair and the score
                pair = (ta,teams[i],s)
                print('Accepted. Total score now: ',score2)
                
                # continue down the tree with remaining teams
                for rest in all_pairs(teams[1:i]+teams[i+1:],costs,score2):
                    # if no teams left to try, go back up
                    if rest==None:
                        yield None
                    
                    # else, combine pairs from lower down, and go back up
                    else:
                        yield [pair] + rest
            
            # else stop searching this branch and go back up
            else:
                yield None
                
            #print 'SL',state_level,current_state,len(teams)
           
    # set current_state ??????
    current_state[state_level]=1
    
    # going back up a level so reduce state_level by 1
    state_level += -1


# prepare list of teams before sending to all_pairs
# return best round

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
    
    print ('CURRENT STATE')
    print (len(current_state),len(teams))
    print (current_state)
    print ('  BEST STATE SO FAR ')
    print (best_state)
    
    # Call all_pairs and start the search for the round with the lowest score:
    match_gen = all_pairs(teams,costs)
    
    ct = 0
    ctn = 0
    better_found = False
    
    for match in match_gen:
        #print ('TEST',current_state,match!=None)
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
        
        # ???? not sure why this is here
        if ctn%1000000==0:
            if ctn>0 and ctn%1000000==0:
                print ("<p>",'STATUS:',ct,ctn,best_score,round(time.time()-starttime,1),'s',"</p>")
        
        # this bit was to exit if it took too long to calculate? more than 240.0 seconds?
        
        #if ctn%10000==0 and round(time.time()-starttime)>240.0:
        #    print ("<p>",'STATUS:',ct,ctn,best_score,round(time.time()-starttime,1),'s',"</p>")
        #    print ("<p>",'STATUS:',best_match,'s',"</p>")
        #    print ("<p>",'TAKING TOO LONG - JSON-EXITING',"</p>")
        #    return [best_state,current_state]
        #    break

    return [best_state,best_match]


if __name__ == '__main__':
    # Testing:
    import random
    
    teams = [0,1,2,3,4,5]
    
    random.seed(12)
    
    costs = []
    for i in range(len(teams)):
        costs.append([])
        for j in range(len(teams)):
            costs[i].append(random.randint(0,10))

    best_state = None
    current_state = None
    best_cost = 99999.0

    print ('DEBUG ')
    print (teams)
    for i in range(len(costs)):
        print (costs[i])
    print (best_state)
    print (current_state)
    print (best_cost)

    results = best_matchups(teams,costs,current_state,best_cost,best_state)

    print ('AFTER RUNNING ')
    print (best_state)
    print (current_state)
    print (best_cost)
    print (results)


