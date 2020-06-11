#!/usr/bin/python3

import ladder_system


team_info = [
# Name, rating, rating again (duplicate)
['Ben',1000,1000],
['Nik',1000,1000],
['Ellie',1000,1000],
['Cullan',1000,1000],
['Dan',1000,1000],
['Notty',1000,1000],
['Vern',1000,1000],
['Zoe',1000,1000],
['Myall',1000,1000],
#['bye1',1000,1000],
#['bye2',1000,1000],

]
                
# round number, then pairs of [name, score], [name, score] etc.
previous_matches = [
[1,['Ben',30],['Nik',43],['Ellie',36]],
[1,['Cullan',41],['Dan',43],['Notty',27]],
[1,['Vern',42],['Zoe',39],['Myall',24]],

[2,['Ben',41],['Notty',33],['Myall',24]],
[2,['Nik',37],['Dan',24],['Vern',23]],
[2,['Ellie',37],['Cullan',26],['Zoe',28]],

[3,['Nik',30],['Notty',43],['Zoe',55]],
[3,['Ellie',26],['Dan',9],['Myall',33]],

[4,['Ben',27],['Dan',34],['Zoe',24]],
[4,['Nik',28],['Cullan',26],['Myall',29]],
[4,['Ellie',45],['Notty',32],['Vern',33]],

[5,['Ellie',30],['Dan',24],['Myall',30.5]],
[5,['Cullan',45],['Zoe',27],['Notty',30]],
[5,['Nik',40],['Vern',1],['Ben',36]],

]


ladder_system.setup_ladder(team_info,previous_matches,3)
    

