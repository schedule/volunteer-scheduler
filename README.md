# Helpline scheduler
Code written in Python 3 finds the best possible schedule for volunteers while incorporating constrains and special requirements using **[CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver)**.

### The problem
Arranging volunteers for a helpline service. There are two types of work done on the same day:
- Phone shift: every day of month.
- Chat shift: Mondays and Wednesdays.

### Constraints:
- Each volunteer gives a list of days they are available.
- Each volunteer has to have 4 days between their shifts.
- One volunteer only does chat because of hearing problems.
- Most volunteers only do phone because they are not qualified for chat.
- Some volunteers do both chat and phone.

### Priorities:
1. Have minimum one volunteer for each day.
2. Fill chat shifts.
3. Have a second volunteer even on phone days.

### Possible special requirements by volunteers:
 - Maximum amount of days for weekend shifts.
 - Wants their shifts to be on separate weeks.
 - Does both chat and phone but prefers chat.
 - Welcomes observer volunteer to work on the same day.
 - Wants to work alone.
 - Cannot work alone.
 - Wants shifts on different weeks.
 - Does not want to work with some other people.

### Objective:
 Maximize filled shifts.

<hr />

## Sample output:

2019 April   -   Distance: 2
<p>2019 April - Distance: 2</p>

<p>Volunteer 1: 13. phone<br />
Volunteer 1: 30. phone<br />
Volunteer 2: 6. phone<br />
Volunteer 2: 12. phone<br />
Volunteer 2: 23. phone<br />
Volunteer 2: 28. phone<br />
Volunteer 3: 22. phone<br />
Volunteer 3: 29. phone<br />
Volunteer 4: 19. phone<br />
Volunteer 4: 27. phone<br />
Volunteer 5: 25. phone<br />
Volunteer 6: 8. phone<br />
Volunteer 6: 15. phone<br />
Volunteer 7: 18. phone<br />
Volunteer 7: 26. phone<br />
Volunteer 8: 3. chat<br />
Volunteer 8: 14. phone<br />
Volunteer 9: 1. phone<br />
Volunteer 9: 10. phone<br />
Volunteer 9: 21. phone<br />
Volunteer 10: 5. phone<br />
Volunteer 10: 16. phone<br />
Volunteer 11: 3. phone<br />
Volunteer 11: 8. chat<br />
Volunteer 12: 4. phone<br />
Volunteer 12: 11. phone<br />
Volunteer 13: 7. phone<br />
Volunteer 13: 15. chat<br />
Volunteer 13: 20. phone<br />
Volunteer 14: 10. chat<br />
Volunteer 14: 22. chat<br />
Volunteer 14: 29. chat<br />
Volunteer 15: 9. phone<br />
Volunteer 15: 17. phone<br />
Volunteer 16: 2. phone<br />
Volunteer 16: 24. phone<br />
Volunteer 17: 6. observer<br />
Volunteer 17: 14. observer<br />
Volunteer 17: 19. observer<br />
Volunteer 17: 26. observer</p>

<p>Remaining capacities: None</p>

<p>Day| P C O<br />
___|___________<br />
 1.| 9 _<br />
 2.| 16 <br />
 3.| 11 8<br />
 4.| 12 <br />
 5.| 10 <br />
 6.| 2 17<br />
 7.| 13 <br />
 8.| 6 11<br />
 9.| 15 <br />
10.| 9 14<br />
11.| 12 <br />
12.| 2 <br />
13.| 1 <br />
14.| 8 17<br />
15.| 6 13<br />
16.| 10 <br />
17.| 15 _<br />
18.| 7 <br />
19.| 4 17<br />
20.| 13 <br />
21.| 9 <br />
22.| 3 14<br />
23.| 2 <br />
24.| 16 _<br />
25.| 5 <br />
26.| 7 17<br />
27.| 4 <br />
28.| 2 <br />
29.| 3 14<br />
30.| 1 <br />
</p>
