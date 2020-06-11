#!/usr/bin/python3

# Terms used in documentation:
#
# 'teams' - referred to by a positive integer (e.g. team 2) - objects that need to be matched up
# 'match' - grouping two or more teams together into a 'match', which will have a 'score'
# 'cost' - number given to each pair of teams, indicating cost of playing each other, higher is worse
# 'score' - number given to the match or round, sum of costs, aim to minimise this
# 'round' - collection of matches where all teams are matched up - has a total score


from timeit import default_timer as timer
import copy


#### best_matchups
# Find the best matchups, given teams, cost matrix, and match_size
# This function to prepares and calls the generator all_matchups

def best_matchups(teams,costs,match_size):
    starttime = timer()
    
    global lowest_score, recursion_level
    
    lowest_score = 99999.0
    recursion_level = -1
    best_match = None

    # Create the generator function, that will be called later:
    match_gen = all_matchups_checks(teams,costs,match_size)
    
    ct = 0
    ctn = 0
    
    print ('Calling generator')
    
    for match in match_gen:
        #print ('TEST',current_state,'Best so far?',match!=None)
        
        if match != None:
            # this match should be the new best (lowest) score:
            ct+=1
            score = 0.0
            for gme in match:
                score+=gme[0]
            if score<lowest_score:
                lowest_score = score
                best_match = copy.deepcopy(match)
        else:
            # this match was not better than current best
            ctn+=1
        
        # Print status updates every 1,000,000 matches:
        if ctn%1000000==0:
            print ('STATUS (# new best rounds, # rounds discarded, best score, elapsed time):')
            print (ct,ctn,lowest_score,round(timer()-starttime,3),'s')
            #print ("<p>",'STATUS:',ct,ctn,lowest_score,"</p>")

    print ('Total Time taken: ',round(timer()-starttime,4))
    
    #for r in best_match:
    #    print (r)
        
    return best_match


#### all_matchups_checks
# Check inputs before calling all_matchups
def all_matchups_checks(teams,costs,match_size=2):
    if match_size < 2:
        print('Match size must be 2 or more')
        return None
    if len(teams)%match_size != 0:
        print('Number of teams must be a multiple of match_size - add a "bye" team if needed')
        return None
    if len(teams) != len(costs):
        print('Costs matrix not the same size as number of teams')
        return None
    if len(teams) != len(costs[0]):
        print('Costs matrix not the same size as number of teams - ER2')
        return None
    
    return all_matchups(teams,costs,match_size)


#### all_matchups
# Function that searches for matchups with lowest total cost
# ** NOTE ** this is recursive!
# ** NOTE ** the 'yield' command is complicated - later calls to this function will return to this spot!
#
# Inputs:
# teams - list of teams that haven't been matched yet - initially len n, but gets shorter
# costs - list of n lists of n floats (n x n marix of costs)
# match_size - how many teams play in each match. default is 2 - pairs.
# score - total score so far
# current_match - passing current match details on for lower recursions
#
# Global variables:
# recursion_level - the "level" of the tree search. top level is 0, should go to n/2
# lowest_score - the lowest score found so far - used to stop searches down branches if score is already above this amount
#
# Function variables:
# starting_index - to account for the first team being added to the match
# new_score - cost of current match
# score2 - update this with score of current match


def all_matchups(teams,costs,match_size=2,score=0.0,current_match=[0.0]):
    
    global recursion_level
    # not sure why lowest_score doesn't need to be declared too - maybe because it's not changed here?
    
    # go 'down' the tree search one level:
    recursion_level += 1
    
    #ws = ' '*recursion_level*4
    #print(ws,'Calling all_matchups, new recursion_level: ',recursion_level)
    #print(ws,'Teams left: ',len(teams))

    # if there aren't any teams left, go back up
    if len(teams) == 0:
        yield teams
        recursion_level += -1
        return
    
    # if no current match, start with first team in list:
    if len(current_match)<2:
        current_match.append([teams[0]])
        starting_index = 1
    else:
        starting_index = 0
        
    # for every other team in team list:
    for i in range(starting_index,len(teams)):
        if (teams[i]>current_match[1][-1]):
            # cost of current adding team to current match
            new_score = 0.0
            # cost vs each team already in match:
            for ts in current_match[1]:
                new_score += costs[ts][teams[i]]

            # only keep going if total score so far is still less than lowest_score, (otherwise skip - no point in continuing)
            # lowest_score is updated in parent function when generator is called
            if new_score+score<lowest_score:
                # update score2 with total score so far
                score2 = new_score+score
                
                # add the team to the match
                current_match[0] += new_score
                current_match[1].append(teams[i])
                
                #if current match is incomplete:
                if len(current_match[1]) < match_size:
                    # continue down the tree with remaining teams
                    for lower_results in all_matchups(teams[starting_index:i]+teams[i+1:],costs,match_size,score2,current_match):
                        # pass results back on up
                        yield lower_results
                else:
                    # continue down with new match:
                    for lower_results in all_matchups(teams[starting_index:i]+teams[i+1:],costs,match_size,score2,[0.0]):
                        # returns None if no teams left, or score worse than lowest_score
                        if lower_results==None:
                            yield None
                        
                        # else, combine results from lower down, and go back up
                        else:
                            yield [current_match] + lower_results
                            
                # remove team from current_match
                current_match[0] += -new_score
                current_match[1].pop()
                
            # else score more than lowest_score, so stop searching this branch and go back up
            else:
                yield None
                
    
    # going back up a level so reduce recursion_level by 1
    recursion_level += -1


def test_matchups_triple():
    # Testing:
    import random
    
    teams = [i for i in range(15)]
    
    random.seed(2)
    
    costs = []
    for i in range(len(teams)):
        costs.append([])
        for j in range(len(teams)):
            #costs[i].append(random.randint(0,10))
            if i>j:
                costs[i].append(0.0+costs[j][i])
            elif i<j:
                costs[i].append(20.0-abs(i-j)+random.randint(0,10))
            else:
                costs[i].append(99.0)

    match_size = 3

    print ('Running test with 16 teams, matching in pairs ')
    
    #print (teams)
    #for i in range(len(costs)):
    #    print (costs[i])

    results = best_matchups(teams,costs,match_size)
    
    print ('RESULTS ')
    for r in results:
        print (r)

if __name__ == '__main__':
    
    #test_matchups_pairs()
    
    test_matchups_triple()
    
    #test_matchups_quad()
    

