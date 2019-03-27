# Helpline scheduler
Code written in Python 3 finds the best possible schedule for volunteers while incorporating constrains and special requirements using **[CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver)**.

### The problem
Arranging volunteers for a helpline service. There are two types of work done on the same day:

Phone shift: every day of month.

Chat shift: Mondays and Wednesdays.

### Constraints:
Each volunteer gives a list of days they are available.

Each volunteer has to have 4 days between their shifts.

One volunteer only does chat because of hearing problems.

Most volunteers only do phone because they are not qualified for chat.

Some volunteers do both chat and phone.

### Priorities:
1. Have minimum one volunteer for each day.
2. Fill chat shifts.
3. Have a second volunteer even on phone days.

### Possible special requirements by volunteers:
 - A certain amount of days of available days are only for weekends.
 - Does both chat and phone but prefers chat.
 - Wants to work alone.
 - Does not want to work with a certain volunteer.
 - Wants shifts on different weeks.

### Objective:
 Maximize filled shifts.
