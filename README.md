# Workshift scheduler for a helpline
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
4. Employ observers on days when there is only phone shift.

### Objective:
 Maximize filled shifts.

<hr>

## Installation

Requires 64-bit Python 3.7

<code>pip3 install helpline-scheduler</code>

## Usage
1. Select your language in config.py: EN/HU/CN
2. Export corresponding data/data_XX.csv file into a spreadsheet, fill in your data, then export back into this file.
3. Execute the program from its directory:

<code>python3 schedule.py</code>

## Output

1. Prints results into the terminal and saves it into schedule_YYYY_MM____YYYYMMDD_hhmm.txt.
2. Saves results into schedule_YYYY_MM____YYYYMMDD_hhmm.csv which can be conveniently imported into a spreadsheet.
