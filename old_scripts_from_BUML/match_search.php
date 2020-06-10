<?php

function best_round($teams,$matches,$debug=False) {
    $tids = array();
    $i=0;
    if ($debug) {
        echo " <p> Teams: ";
        foreach ($teams as $team) {
            $tids[$i] = $team->nid;
            $i++;
            echo ' <p> ',$team->nid,' ';
            echo $team->title,'    </p>';
        }
        echo " </p> ";
    }
    $costs = calc_costs($teams,$matches);
    if ($debug) {dpm($costs);dpm($teams);}
    
    if ($debug) {echo "<p>TEST</p>";}
    
    $gvals = node_load(1400);
    // this node has the following stored variables:
    // "field_best_round_cost" is the best cost found so far. If negative, means search not started.
    // "field_best_round_state" is a list of integers which is the state for the best round.
    // "field_current_state_round_calc" is a list of integers which is the state of the search. 

    $best_cost = (float) get_if_set($gvals->field_best_round_cost['und'][0]['value'],-999);
    if ($best_cost<=0.0) {
        $best_cost = 99999999.0;
        $current_state = null;
        $best_round_state = null;
    } else {
        $current_state = $gvals->field_current_state_round_calc['und'];
        $best_round_state = $gvals->field_best_round_state['und'];
        if ($current_state[0]<=0) {
            // If the first current_state is negative or zero, means search has been completed
            return match_from_state($teams,$costs,$best_round_state);
        }
    }
    
    if ($debug) {echo "<p>".'Starting Cost: '.$best_cost."</p>";}
    
    $current_state_json = escapeshellarg(json_encode(nodestate2state($current_state)));
    $best_state_json = escapeshellarg(json_encode(nodestate2state($best_round_state)));
    $best_cost_str = (string) $best_cost;
    $costs_json = escapeshellarg(json_encode($costs));
    $teams_json = escapeshellarg(json_encode($tids));
    
    $args = ' ' . $best_cost . ' '. $best_state_json . ' ' . $current_state_json . ' ' . $teams_json . ' '. $costs_json;
    //$result=null;
    $result = shell_exec('python /home/qudaorg/public_html/buml-dev/sites/default/files/scripts/core/league_best_round_L1.py ' . $args );
    if ($debug) {echo " OUTPUT "; echo $result;}
    if ($result==null) {
        echo "<p>NULL RESULTS FOUND; RUN LOCALLY USING THE FOLLOWING PARAMETERS:</p>";
        if ($debug) {echo "<p>".'INITIAL STATE: '.$current_state_json."</p>";}
        //echo "<p>".'TESTING: '.$best_cost.' '.$best_round_first_pair.' '.$current_round_calc_pair ."</p>";
        if ($debug) {echo "<p>".' JSON ARGS: '.$args." END JSON ARGS </p>";}
        if ($debug) {
            echo "<p>".' Teams: ';
            foreach ($teams as $t) {
                echo strval($t->nid).":'".strval($t->title)."',\n";
            }
            echo "</p>";
        }
        echo "<p>**** USING RESULTS PASTED IN match_search.php SCRIPT INSTEAD ****</p>";
        $result = paste_json_results_here();
        echo $result;
    }
    $res = explode('JSON-FOLLOWING',$result);
    $results = json_decode($res[1]);
    $best_state_array = $results[0];
    
    // MANUALLY SET STATE HERE:
    //$best_state_array = array(7,5,3,1,7,5,3,1,7,5,3,1);
    
    $best_round = match_from_state($teams,$costs,$best_state_array);
    if (strstr($result,'JSON-EXITING')!=False) {
        // Search finished early, so need to save state:
        echo "<p>".'Search Finished Early - save state:  BEST'."</p>";
        $current_state_array = $results[1];
        
        display_matches_from_state($teams,$costs,$best_state_array);
        echo "<p>".'Search Finished Early - save state:  CURRENT'."</p>";
        display_matches_from_state($teams,$costs,$current_state_array);
        
        $sum = 0;
        foreach (match_from_state($teams,$costs,$best_state_array) as $match) {
            $sum += (float) $match[2];
        }
        $gvals->field_current_state_round_calc['und'] = state2nodestate($current_state_array);
        if ($sum < $best_cost) {
            // reset best cost, and best_round_first_pair
            $gvals->field_best_round_cost['und'][0]['value'] = $sum;
            $gvals->field_best_round_state['und'] = state2nodestate($best_state_array);
        }

    } else {
        
        // Best round has been found:
        echo "<p>".'SUGGESTED ROUND DETERMINED'."</p>";
        display_matches_from_state($teams,$costs,$best_state_array);
        $gvals->field_best_round_cost['und'][0]['value'] = -1.0;
        $gvals->field_current_state_round_calc['und'] = array(array('value'=>-1));
        $gvals->field_best_round_state['und'] = state2nodestate($best_state_array);
    }
    node_save($gvals);
    return $best_round;
}

function match_from_state($teams,$costs,$state) {
    $rteams = array_keys($costs);
    $match = array();
    $i=0;
    while  ($i<count($state)) { //(count($rteams)>=2) {
        $j = $state[$i];
        if (gettype($j)=='array') {
            $j = $j['value'];
        }
        $match[] = array($rteams[0],$rteams[$j],$costs[$rteams[0]][$rteams[$j]]);
        $rteams = array_merge(array_slice($rteams,1,$j-1,True),array_slice($rteams,$j+1,count($rteams),True));
        $i++;
    }
    return $match;
}

function state2nodestate($state) {
    $i=0;
    while ($i<count($state)) {
        $state[$i] = array('value'=>$state[$i]);
        $i++;
    }
    return $state;
}

function nodestate2state($state) {
    if (array_key_exists('und',$state)) {
        $state = $state['und'];
    }
    $i=0;
    while ($i<count($state)) {
        $state[$i] = (int) $state[$i]['value'];
        $i++;
    }
    return $state;
}

function display_matches_from_state($teams,$costs,$state){
    $matches = match_from_state($teams,$costs,$state);
    $sum = 0;
        foreach ($matches as $match) {
            $sum += (float) $match[2];
        }
    echo "<p> Total Cost is: ".$sum."</p>";
    foreach ($matches as $match) {
        $t1 = $teams[$match[0]];
        $t2 = $teams[$match[1]];
        echo "<p> Game: " . $t1->title . ' (' . $t1->field_rating['und'][0]['value'] . ') vs ' . $t2->title . ' (' . $t2->field_rating['und'][0]['value'] . ')  cost: ' . $match[2];
        echo "</p>";
    }
}


/**
* Function - calculates game history and venue history, and makes badness matrix
*/
function calc_costs($teams,$matches) {    
    $last = array(); // when did the teams last play
    foreach ($teams as $team) {
        $last[$team->nid] = array();
        foreach ($teams as $team2){
            $last[$team->nid][$team2->nid] = 999;
        }
    }
    
    $number = array(); // how many times have the teams played each other
    foreach ($teams as $team) {
        $number[$team->nid] = array();
        foreach ($teams as $team2){
            $number[$team->nid][$team2->nid] = 0;
            }
        }
    
    $current = 0;
    
    $fields_n = views_get_view_result('venues_list', 'master');
    $fields = array();
    foreach ($fields_n as $f) {
        $fields[] = $f->nid;
    }
    
    foreach ($matches as $result) {
        $round_number = (int) get_if_set($result->node_field_data_field_round__field_data_field_round_id_field, 0);
        if ($round_number>$current) {
            $current=$round_number;
		}
            
        // Get variables for easier reference.
        $home_team = $result->field_field_team[0]['raw']['node']; 
        $away_team = $result->field_field_team_1[0]['raw']['node'];
        $nid1 = $home_team->nid;
        $nid2 = $away_team->nid;
        
        // Round number when teams last played.
        $last[$nid1][$nid2] = -$round_number;
        $last[$nid2][$nid1] = -$round_number;
        $number[$nid1][$nid2] += 1;
        $number[$nid2][$nid1] += 1;
        
        $rfull = node_load($result->nid);
        $venueid = $rfull->field_match_field['und'][0]['tid'];
        $venuet = taxonomy_term_load($venueid);
        $venue = $venuet->field_venue['und'][0]['nid'];
        
        for ($i = 0; $i < count($fields); $i++) {
            if ($venue==$fields[$i]) {
                $teams[$nid1]->field_venue_history['und'][$i]['value'] += 1;
                $teams[$nid2]->field_venue_history['und'][$i]['value'] += 1;
                }
            }
        }
    
    // Round in which the teams played each other - change to how many weeks ago this was.
    foreach ($teams as $team) {
        foreach ($teams as $team2) {
            if ($last[$team->nid][$team2->nid]<0) {
                $last[$team->nid][$team2->nid] += $current + 1; // + 100*$number[$team->nid][$team2->nid];
			}
		}
	}
    
    $costs = array(); // when did the teams last play
    foreach ($teams as $team1) {
        $costs[$team1->nid] = array();
        foreach ($teams as $team2){
            $lastt = $last[$team1->nid][$team2->nid];
            $numbert = $number[$team1->nid][$team2->nid];
            $costs[$team1->nid][$team2->nid] = match_cost($team1,$team2,$lastt,$numbert);
		}
	}
    
    foreach ($teams as $team) {
        node_save($team);
    }
	
    return $costs;
    }

/**
* Calculates current venue ratios compared to desired. For each venue, positive = want to play there more, negative = play less.
*/
function calc_current_venue_prefs($team,$fields_n=null) {
    if ($fields_n==null) {
        $fields_n = views_get_view_result('venues_list', 'master');
    }
    
    $played = 0;
    $history = $team->field_venue_history['und'];
    //$fields_n = views_get_view_result('venues_list', 'master');
    foreach ($history as $vh) {
        $played += $vh['value'];
    }
    if ($played<1) {
        $played = 1;
    }
    $actual = array();
    $desired = $team->field_venue_desired['und'];
    
    for ($i = 0; $i < count($fields_n); $i++) {
        $actual[] = $desired[$i]['value']*1.0 - $history[$i]['value']/$played;
    }
    return $actual;
}

function get_venue_prefs($team,$fields_n) {
    //$fields_n = views_get_view_result('venues_list', 'master');

    $actual = array();
    $desired = $team->field_venue_desired['und'];
    
    for ($i = 0; $i < count($fields_n); $i++) {
        $actual[] = $desired[$i]['value']*1.0;
    }
    return $actual;
}
/**
* Function that compares field preferences, to give a weighting factor.
*/
function field_cost($team1,$team2) {
    $fields_n = views_get_view_result('venues_list', 'master');
    $fd1 = get_venue_prefs($team1,$fields_n);
    $fd2 = get_venue_prefs($team2,$fields_n);
    
    $fp1 = calc_current_venue_prefs($team1,$fields_n);
    $fp2 = calc_current_venue_prefs($team2,$fields_n);
    
    // Checks each venue. If there is a commom desired venue, returns 0, if not, return vaires.
    // if teams have pref over a certain amount at different venues, returns 10.0:
    $cut = 0.51;
    $cutm = -2.26;
    $fp1o = False;
    $fp2o = False;
    
    for ($i = 0; $i < count($fd1); $i++) {
		if ($fd1[$i]>$cut) {
			$fp1o = True;
            if ($fd2[$i]<$cutm) {
                return 1.0;
            }
		}
		elseif ($fd2[$i]>$cut) {
			$fp2o = True;
            if ($fd1[$i]<$cutm) {
                return 1.0;
            }
		}
	}
	if ($fp1o AND $fp2o) {
		return 1.0;
	}
        
    //add a small amount to allow even slightly unfavourable venues to be OK.
    // based on number of games played - so that early on it doesn't matter:
    $n = $team1->field_matches_played['und'][0]['value'] + $team2->field_matches_played['und'][0]['value'];
    if ($n<5) {
		$tol = 1.5;
	}
	elseif ($n<10) {
		$tol = 0.2;
	}
	else {
		$tol = 0.1;
	}
    
    for ($i = 0; $i < count($fp1); $i++) {
		if ($fp1[$i]+$tol > 0.0) {
			if ($fp2[$i]+$tol > 0.0) {
				return 0.0;
			}
		}
	}
	
	return 0.3;
}

/**
* Function that returns factor based on how recently the teams played
*/
function replay_cost($team1,$team2,$last,$number) {
    // some default values:
    $too_soon = 2;
    $season_length = 17;
    $minimum_maxreplay = 3;
    

    $nid1 = $team1->nid;
    $nid2 = $team2->nid;

    if ($nid1==$nid2) {
        // same team - avoid
        return 10.0;
    }
    if ($number==0) {
        //never played
        return 0.0;
    }
    if ($last<$too_soon) {
        //played last week or the week before
        return 10.0;
    }

    # used lowest team replay:
    $replay = $team1->field_replay_period['und'][0]['value'];
    $replay2 = $team2->field_replay_period['und'][0]['value'];
    if ($replay2<$replay) {
        $replay = $replay2;
    }
    
    if ($number>max($season_length/$replay,$minimum_maxreplay)) {
        //played too much
        return 10.0;
    }
    
    if ($last>$replay) {
        //past replay period:
        return 0.0;
    }

    return ($replay - $last)/($replay - $too_soon);
    }

/**
* Function the combines all the factors and returns the total badness for the match.
*/
function match_cost($team1,$team2,$last,$number) {
    $rc = replay_cost($team1,$team2,$last,$number);
    $fc = field_cost($team1,$team2);
    
    $rrc = abs($team1->field_rating['und'][0]['value'] - $team2->field_rating['und'][0]['value']);
    
    $rct = $rrc + ($rc+$fc)*100.0;
    
    if ($fc>1000.0) {
        echo ' TTTTT Field Cost '.$team1->title.' '.$team2->title.' '.$fc.' ';
    }
    
    if ($team1->field_status['und'][0]['value']=='Retired') {
        $rct = 10000.0;
    }
    if ($team2->field_status['und'][0]['value']=='Retired') {
        if ($rct>=10000.0) {
            $rct = 0.0;
        } else {
            $rct = 10000.0;
        }
    }
    
    return $rct;
}

function display_round_details($teams,$round) {
    foreach ($round as $match) {
        $t1 = $teams[$match[0]];
        $t2 = $teams[$match[1]];
        echo "<p> Game: " . $t1->title . ' (' . $t1->field_rating['und'][0]['value'] . ') vs ' . $t2->title . ' (' . $t2->field_rating['und'][0]['value'] . ')  cost: ' . $match[2];
        echo '  Venue: '.$match[4]->node_title.' ';
        echo "</p>";
    }
}

function array2string($array) {
    $s=' ';
    foreach ($array as $a) {
        $s.=$a.' ';
    }
    return $s;
}

function assign_venues($teams,$round,$debug=False,$method=1) {
	// $round is a list of games in the round to be assigned
    //AJSC, Griffith, Gap, Easts, QUT, Grange
    $fields_n = views_get_view_result('venues_list', 'master');
    $fields = array();
    $fsize = array();
    $fnumb = array();
    foreach ($fields_n as $f) {
        $fields[] = $f->nid;
        $fn = node_load($f->nid);
        //dpm($fn);
        $fsize[] = get_if_set($fn->field_venue_capacity['und'][0]['value'],0);
        $fnumb[] = 0;
    }
    //$fsize = array(4,2,2,3,3);
    if ($debug){
		for ($i = 0;$i<count($fields); $i++) {
			echo "<p>".'Field: '.$fields_n[$fields[$i]]->node_title.' Capacity: '.$fsize[$i]."</p>";
		}
	}
    $assigned = array();
    $i=0;
    for ($i = 0; $i < count($round); $i++) {
        $assigned[] = False;
        $v1 = calc_current_venue_prefs($teams[$round[$i][0]]);
        $v2 = calc_current_venue_prefs($teams[$round[$i][1]]);
        if ($debug) {
            echo "<p>".'Team '.$teams[$round[$i][0]]->title.' '.array2string($v1)."</p>";
            echo "<p>".'Team '.$teams[$round[$i][1]]->title.' '.array2string($v2)."</p>";
        }
        $j=0;
        $round[$i][] = array();
        for ($j = 0; $j < count($v1); $j++) {
            if ($method==1) {
                $round[$i][3][] = $v1[$j]+$v2[$j];
            } else {
                $round[$i][3][] = max($v1[$j],$v2[$j]);
            }
        }
    }
    $i=0;
    foreach ($round as $temp) {
        $highest_fp = -10.0;
        $gm = -1;
        $f = -1;
        for ($i = 0; $i < count($round); $i++) {
            if ($assigned[$i]==False) {
                if (($teams[$round[$i][0]]->title!='BYE' and $teams[$round[$i][1]]->title!='BYE') ){ // or (($i==count($round)-1) and ($gm==-1))) {
                    for ($j = 0; $j < count($round[$i][3]); $j++) {
                        if ($fnumb[$j]<$fsize[$j]) {
                            if ($round[$i][3][$j]>$highest_fp) {
                                $highest_fp = $round[$i][3][$j];
                                $gm = $i;
                                $f = $j;
                            }
                        }
                    }
                }
            }
        }
        if ($debug) {
            echo "<p>".$teams[$round[$gm][0]]->title.' vs '.$teams[$round[$gm][1]]->title."</p>";
            echo "<p>".'ASSIGNED to '.$fields_n[$f]->node_title.' ('.array2string($round[$gm][3]).')'."</p>";
        //Assign game to venue:
        }
        $round[$gm][] = $fields_n[$f];
        $fnumb[$f]+=1;
        $assigned[$gm] = True;
    }
    display_round_details($teams,$round);
}

function paste_json_results_here() {
    //insert results:
    //echo "<p>**** NO RESULTS PASTED ****</p>";
    //$results = '';

    $results = 'JSON-FOLLOWING
[[1, 1, 1, 1, 1, 1, 1, 2, 2, 5, 3, 2, 1], [["45", "2719", 12], ["28", "62", 2], ["1500", "2718", 1], ["2274", "2716", 2], ["49", "56", 1], ["2738", "2495", 0], ["59", "2717", 6], ["453", "2237", 13], ["626", "815", 13], ["2720", "599", 31], ["2715", "984", 6], ["1402", "2722", 21], ["2721", "2737", 32]]]';

    return $results;
}
