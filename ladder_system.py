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

def best_matchups(teams,costs,match_size,quiet=True):
    starttime = timer()
    
    global lowest_score, recursion_level
    
    lowest_score = 99999.0
    recursion_level = -1
    best_match = None

    # Create the generator function, that will be called later:
    match_gen = all_matchups_checks(teams,costs,match_size)
    
    ct = 0
    ctn = 0
    
    if not quiet: print ('Calling generator')
    
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
            if not quiet: 
                print ('STATUS (# new best rounds, # rounds discarded, best score, elapsed time):')
                print (ct,ctn,lowest_score,round(timer()-starttime,3),'s')
                #print ("<p>",'STATUS:',ct,ctn,lowest_score,"</p>")

    if not quiet: print ('Total Time taken: ',round(timer()-starttime,4))
    
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

def test_matchups_pairs():
    #NOT WORKING
    print('NOT WORKING - does not produce results')
    return False
# Testing:
    import random
    
    teams = [i for i in range(14)]
    
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

    match_size = 2

    print ('Running test with 14 teams, matching in groups of 2 ')
    
    #print (teams)
    #for i in range(len(costs)):
    #    print (costs[i])

    results = best_matchups(teams,costs,match_size,quiet=True)
    
    print (results)
    
    correct_results = [[8.0, [0, 12]], [8.0, [1, 13]], [14.0, [2, 10]], [16.0, [3, 9]], [19.0, [4, 7]], [19.0, [5, 8]], [23.0, [6, 11]]]
    
    results_same = True
    for i in range(len(results)):
        if (results[i][0]!=correct_results[i][0]):
            results_same = False
            break
            #raise Exception('Error: results different')
        for j in range(len(results[i][1])):
            if (results[i][1][j]!=correct_results[i][1][j]):
                results_same = False
                break
                #raise Exception('Error: results different')
        if not results_same: break
        
    if results_same:
        print ('-- Results correct --')
    else:
        print ('ERROR, results different: teams 14, match size 2')
        print ('Results:')
        for r in results:
            print(r)
        print ('Expected Results:')
        for r in correct_results:
            print(r)
    
    return results_same

def test_matchups_triple():
    # Testing:
    import random
    
    teams = [i for i in range(12)]
    
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

    print ('TEST: Running with 12 teams, matching in groups of 3')
    
    #print (teams)
    #for i in range(len(costs)):
    #    print (costs[i])

    results = best_matchups(teams,costs,match_size,quiet=True)
    
    correct_results = [[57.0, [0, 4, 7]], [56.0, [1, 5, 9]], [54.0, [2, 6, 10]], [49.0, [3, 8, 11]]]
    
    results_same = True
    for i in range(len(results)):
        if (results[i][0]!=correct_results[i][0]):
            results_same = False
            break
            #raise Exception('Error: results different')
        for j in range(len(results[i][1])):
            if (results[i][1][j]!=correct_results[i][1][j]):
                results_same = False
                break
                #raise Exception('Error: results different')
        if not results_same: break
    
    if results_same:
        print ('-- Results correct --')
    else:
        print ('ERROR, results different: teams 15, match size 3')
        print ('Results:')
        for r in results:
            print(r)
        print ('Expected Results:')
        for r in correct_results:
            print(r)
    
    return results_same

def test_matchups_quad():
    #NOT WORKING
    print('NOT WORKING - does not produce results')
    return False
    

## team_info
# position in list is number
# name - CANNOT START WITH 'bye' - will be treated as a 'bye'
# rating - higher is better
# starting_rating

# Cost matrix:
# if name is bye:
# - cost 9999 to play another 'bye' team
# - ignore rating in cost

# Previous results
# need:
# team names and scores
# round number


def setup_ladder(team_info,previous_matches,match_size=2):
    # team_info: team name, starting rating, updated ranking
    # previous_matches: round number, [team, score], [team, score] etc.
    
    costs = [[0.0 for i in range(len(team_info))] for j in range(len(team_info))]
        
    team_info,costs = update_ratings(previous_matches,team_info,costs)
    
    print ('One pass ratings:')
    for t in team_info:
        print(*t[0:2],sep=",")
        
    # rerun rating update to try to see if ratings good for all matches
    for i in range(3):
        team_info,costs_discard = update_ratings(previous_matches,team_info,costs)
    
    print ('Multipass ratings:')
    for t in team_info:
        print(*t[0:2],sep=",")
        
    # now update cost matrix with rating differences:
    for i in range(len(team_info)):
        if team_info[i][0][:3]=='bye':
            for j in range(len(team_info)):
                if team_info[j][0][:3]=='bye':
                    costs[i][j] = 99999.0
        else:
            for j in range(len(team_info)):
                if team_info[j][0][:3]!='bye':
                    costs[i][j] += abs(team_info[i][1]-team_info[j][1])
    
    
    for c in costs:
        print (c)
        
    
    print ('Latest ratings:')
    for t in team_info:
        print(*t[0:2],sep=",")
            
    results = best_matchups([i for i in range(len(team_info))],costs,match_size,quiet=True)
    
    print ('Next round of matches:')
    for r in results:
        print (*[team_info[i][0] for i in r[1]], sep = ", ,")
        
def update_ratings(previous_matches,team_info,costs):
    
    bye_teams = []
    
    team_dict = {}
    
    for i in range(len(team_info)):
        team_dict[team_info[i][0]] = i
        if team_info[i][0][:3] == 'bye':
            bye_teams.append(i)
    
    #print('bye teams: ',bye_teams)
    
    replay_cost = 500.0 #will be multiplied by round_number
    
    cur = 0

    #print ('Previous matches')
    for r in previous_matches:
        n_teams = len(r)-1
        
        #print(r)
        #if r[0]>cur:
        #    cur = r[0]
        #    print ('Latest ratings: r',cur-1)
        #    for t in team_info:
        #        print(*t[0:2],sep=",")
        
        for i in range(n_teams):
            # team number:
            teami = team_dict[r[i+1][0]]
            for j in range(n_teams):
                # team number:
                teamj = team_dict[r[j+1][0]]
                if i!=j:
                    # handle byes: add replay_cost for all bye teams
                    if (teami in bye_teams):
                        for bt in bye_teams:
                            costs[bt][teamj] += replay_cost*(20+r[0])
                    elif (teamj in bye_teams):
                        for bt in bye_teams:
                            costs[teami][bt] += replay_cost*(20+r[0])       
                    else:
                        # add replay cost - to avoid playing same teams again
                        costs[teami][teamj] += r[0]*replay_cost
                        
                        # now update team i rating, ignoring byes
                        team_info[teami][2] += calc_rating_change(r[i+1][1],r[j+1][1],team_info[teami][1],team_info[teamj][1])
        
        # only after round calculated, update actual ratings:
        for i in range(len(team_info)):
            team_info[i][1] = team_info[i][2]
            
    return team_info,costs
             
def calc_rating_change(score1,score2,rating1,rating2):
    #####
    #
    # Win?  rating higher    get rating b   score factor        Net
    # yes   yes                 -ive            +ive            small change
    # yes   no                  +ive            +ive            big change
    # no    yes                 -ive            -ive            big negative
    # no    no                  +ive            -ive
    
    # summary:
    # if win: rating increase
    # add amount based on negative of rating difference
    # add amount based on score (negative if you lost) - equal to rating difference
    
    
    win_bonus = 3 # amount your rating goes up (or down) if score higher than someone with a higher rating, or vice-versa
    score_rating_change = 3.0 #multiply by the factor based on score difference
    
    add_to_score = 0.0
    if min(score1,score2) < 1:
        add_to_score = abs(min(score1,score2)) # add this to sure all scores positive
    
    # ratio of scores:
    # 1.0 to 2.0, no benefit from beating by anything more than double
    score_factor = min(2.0,(max(score1,score2)+add_to_score)/(min(score1,score2)+add_to_score)) # minimum value is 0.5
    
    
    # rating factor - between 1.0 and 2.0
    rating_factor = min(abs(rating1-rating2)/100.0,1.0)+1.0
    
    # your rating decreases by rating factor, increases by score factor
    # so if your rating is half your opponents, but you score twice as much
    
    
    
    if rating1>rating2:
        if score1<=score2:
            return -win_bonus-int(score_rating_change*(score_factor+rating_factor)+0.5)
        else:
            return win_bonus+int(score_rating_change*(score_factor-rating_factor)+0.5)
    elif rating1<rating2:
        if score1>=score2:
            return win_bonus+int(score_rating_change*(score_factor+rating_factor)+0.5)
        else:
            return -win_bonus-int(score_rating_change*(score_factor-rating_factor)+0.5)
    else:
        if score1>score2:
            return win_bonus+int(score_rating_change*(score_factor)+0.5)
        elif score1<score2:
            return -win_bonus-int(score_rating_change*(score_factor)+0.5)
    
    return 0


def trial_run():
    team_info = [
        
    ['team0name',1000,1000],
    ['team1name',1000,1000],
    ['team2name',1000,1000],
    ['team3name',1000,1000],
    ['team4name',1000,1000],
    ['team5name',1000,1000],
                     
                ]
                
# round number, [team, score], [team, score] etc.
    previous_matches = [
        
    [1,['team0name',25],['team1name',52],['team2name',26]],
    [1,['team3name',23],['team4name',24],['team5name',15]],

                        ]
    
    setup_ladder(team_info,previous_matches,3)
    
    
if __name__ == '__main__':
    
    #test_matchups_pairs()
    
    #test_matchups_triple()
    
    #test_matchups_quad()
    
    trial_run()
    
