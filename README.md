# Helpline scheduler
Code written in Python finds the best possible schedule for volunteers while incorporating constrains and special requirements using **[CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver)** (Constraint Programming - boolean SATisfiability problem Solver).

### The problem
Arranging volunteers for a helpline service. There are three types of work that could be done on the same day:
- Phone shift: every day of month.
- Chat shift: Mondays and Wednesdays.
- Observer shift: any day.

### Constraints:
- Each volunteer gives a list of days they are available.
- Each volunteer has to have 4 days between their shifts.
- One volunteer only does chat.
- Most volunteers only do phone because they are not qualified for chat.
- Some volunteers do both chat and phone.
- An observer volunteer works whenever one is available and the volunteers doing the other shifts all welcome an observer.

### Priorities:
1. Have minimum one volunteer for each day.
2. Fill chat shifts.
3. Have a second volunteer even on phone days.

### Possible specifications:
 - Maximum amount of weekend shifts.
 - Shifts to be on separate weeks.
 - Prefers chat shift while eligible for both chat and phone.
 - Welcomes observer volunteer.
 - Wants to work alone.
 - Cannot work alone.
 - Wants shifts on different weeks.
 - Does not want to work with some other people.

### Objective:
 Maximize filled shifts.
