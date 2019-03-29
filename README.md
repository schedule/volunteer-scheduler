# Helpline scheduler
Code written in Python finds the best possible schedule for volunteers while incorporating constrains and special requirements using **[CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver)** (Constraint Programming - boolean SATisfiability problem Solver).

Java version is in development.

### The problem
Arranging volunteers for a helpline service for the period of one month. 

There are three types of work that could be done on the same day:
- Phone shift: Every day.
- Chat shift: Mondays and Wednesdays.
- Observer shift: Any day.

### Constraints:
Properties of each volunteer:
- Available days.
- Function: doing phone, chat, both or observation for training purposes.
- Maximum amount of weekend shifts.
- Whether their shifts have to be on separate weeks.
- Whether they welcome observers.
- Whether they want to work alone.
- Whether they cannot yet work alone.
- List of people they do not want to work with.

Each volunteer has to have 4 days between their shifts.
 
### Priorities:
1. Have minimum one volunteer for each day.
2. Fill chat shifts.
3. Have a second volunteer even on phone days.
4. Employ observers if possible.

### Objective:
 Maximize filled shifts.

</hr>

## Sample output

2019 April 

Volunteer 1: 13. phone

Volunteer 1: 30. phone

<...>

Volunteer 17: 14. observer


Remaining capacities: None

Day|  P  C  O
___|___________
 1.|  9  _ 
 2.| 16    
 3.| 11  8 
 4.| 12    
 5.| 10    
 6.|  2    17 
 7.| 13    
 8.|  6 11 
 9.| 15    
10.|  9 14 
11.| 12    
12.|  2    
13.|  1    
14.|  8    17 
15.|  6 13 
16.| 10    
17.| 15  _ 
18.|  7    
19.|  4    17 
20.| 13    
21.|  9    
22.|  3 14 
23.|  2    
24.| 16  _ 
25.|  5    
26.|  7    17 
27.|  4    
28.|  2    
29.|  3 14 
30.|  1    
