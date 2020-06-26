#!/usr/bin/python3

import ladder_system_glicko
import copy

variability = 100

team_info = [
# Name, rating, variability, playing next round?
['Ben',1500,variability,True],
['Nik',1500,variability,True],
['Ellie',1500,variability,False],
['Cullan',1500,variability,True],
['Dan',1500,variability,False],
['Notty',1500,variability,True],
['Vern',1500,variability,True],
['Zoe',1500,variability,False],
['Myall',1500,variability,True],
['Gladish',1500,variability,True],
['Nat',1500,variability,False],
['Dusty',1500,variability,False],
['Gareth',1500,variability,False],
['bye1',1500,variability,True],
['bye2',1500,variability,False],

# [ 'Ben' , 1517 , 97 ,True],
# [ 'Nik' , 1604 , 98 ,True],
# [ 'Ellie' , 1607 , 98 ,True],
# [ 'Cullan' , 1442 , 98 ,True],
# [ 'Dan' , 1500 , 97 ,True],
# [ 'Notty' , 1390 , 98 ,True],
# [ 'Vern' , 1459 , 97 ,True],
# [ 'Zoe' , 1432 , 97 ,True],
# [ 'Myall' , 1583 , 97 ,True],
# ['bye1',1500,variability,False],
# ['bye2',1500,variability,False],

]

# To add costs to player matchups:
# [player1, player2, cost]
additional_costs = [

['Dan','Ellie',200.0],
['Nat','Gareth',200.0],
['Nik','Zoe',200.0],
['Notty','Vern',200.0],


]

# round number, then pairs of [name, score], [name, score] etc.
previous_matches = [
# [1,['Ben',30],['Nik',43],['Ellie',36]],
# [1,['Cullan',41],['Dan',43],['Notty',27]],
# [1,['Vern',42],['Zoe',39],['Myall',24]],

# [2,['Ben',41],['Notty',33],['Myall',24]],
# [2,['Nik',37],['Dan',24],['Vern',23]],
# [2,['Ellie',37],['Cullan',26],['Zoe',28]],

# [3,['Nik',30],['Notty',43],['Zoe',55]],
# [3,['Ellie',26],['Dan',9],['Myall',33]],

# [4,['Ben',27],['Dan',34],['Zoe',24]],
# [4,['Nik',28],['Cullan',26],['Myall',29]],
# [4,['Ellie',45],['Notty',32],['Vern',33]],

# [5,['Ellie',30],['Dan',24],['Myall',30.5]],
# [5,['Cullan',45],['Zoe',27],['Notty',30]],
# [5,['Nik',40],['Vern',1],['Ben',36]],

# [1,['Ben',42],['Nik',24],['Gareth',37]],
# [1,['Cullan',16],['Dan',33],['Notty',37]],
# [1,['Zoe',12],['Myall',15],['Gladish',9]],
# [1,['Nat',32],['Dusty',40],['Ellie',46]],

# [2,['Ben',24],['Notty',19],['Myall',50]],
# [2,['Nik',19],['Zoe',39],['Dusty',39]],
# [2,['Ellie',33.5],['Dan',24],['Gareth',33]],
# [2,['Cullan',31],['Gladish',42.5],['Nat',42]],

# [3,['Ben',36],['Dan',18],['Gladish',31]],
# [3,['Nik',29],['Ellie',43.5],['Cullan',43]],
# [3,['Notty',33],['Zoe',45],['Nat',24]],
# [3,['Myall',33],['Dusty',39],['Gareth',43]],

# [4,['Ben',24],['Cullan',34],['Dusty',22]],
# [4,['Nik',45],['Dan',31],['Nat',5]],
# [4,['Ellie',22],['Zoe',24],['Myall',30]],
# [4,['Notty',27],['Gladish',27],['Gareth',38]],

# [5,['Ben',18],['Ellie',36],['Zoe',18]],
# [5,['Nik',37],['Notty',42],['Nat',28]],
# [5,['Cullan',27],['Myall',37],['Gareth',27]],
# [5,['Dan',57],['Gladish',33],['Dusty',39]],

[1,['Notty',54],['Gladish',32],['Myall',55]],
[1,['Ben',59],['Vern',49],['Cullan',45]],

[2,['Ben',48],['Notty',46],['Myall',89],['bye1',0]],
[2,['Nik',58],['Cullan',89],['Vern',16],['Gladish',26]],

[3,['Ben',89],['Notty',88],['Gladish',98]],
[3,['Nik',59],['Cullan',62],['Myall',46]],

[4,['Ben',27],['Nik',47],['Cullan',31],['Notty',41]],
[4,['Vern',3],['Myall',74],['Gladish',13],['bye1',0]],

]


ladder_system_glicko.setup_ladder(team_info,previous_matches,match_size=4,additional_costs=additional_costs)
    

