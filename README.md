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

<p>2019&npspApril&npsp-&npspDistance:&npsp2</p>

<p>Volunteer&npsp1:&npsp13.&npspphone<br/>
Volunteer&npsp1:&npsp30.&npspphone<br/>
Volunteer&npsp2:&npsp6.&npspphone<br/>
Volunteer&npsp2:&npsp12.&npspphone<br/>
Volunteer&npsp2:&npsp23.&npspphone<br/>
Volunteer&npsp2:&npsp28.&npspphone<br/>
Volunteer&npsp3:&npsp22.&npspphone<br/>
Volunteer&npsp3:&npsp29.&npspphone<br/>
Volunteer&npsp4:&npsp19.&npspphone<br/>
Volunteer&npsp4:&npsp27.&npspphone<br/>
Volunteer&npsp5:&npsp25.&npspphone<br/>
Volunteer&npsp6:&npsp8.&npspphone<br/>
Volunteer&npsp6:&npsp15.&npspphone<br/>
Volunteer&npsp7:&npsp18.&npspphone<br/>
Volunteer&npsp7:&npsp26.&npspphone<br/>
Volunteer&npsp8:&npsp3.&npspchat<br/>
Volunteer&npsp8:&npsp14.&npspphone<br/>
Volunteer&npsp9:&npsp1.&npspphone<br/>
Volunteer&npsp9:&npsp10.&npspphone<br/>
Volunteer&npsp9:&npsp21.&npspphone<br/>
Volunteer&npsp10:&npsp5.&npspphone<br/>
Volunteer&npsp10:&npsp16.&npspphone<br/>
Volunteer&npsp11:&npsp3.&npspphone<br/>
Volunteer&npsp11:&npsp8.&npspchat<br/>
Volunteer&npsp12:&npsp4.&npspphone<br/>
Volunteer&npsp12:&npsp11.&npspphone<br/>
Volunteer&npsp13:&npsp7.&npspphone<br/>
Volunteer&npsp13:&npsp15.&npspchat<br/>
Volunteer&npsp13:&npsp20.&npspphone<br/>
Volunteer&npsp14:&npsp10.&npspchat<br/>
Volunteer&npsp14:&npsp22.&npspchat<br/>
Volunteer&npsp14:&npsp29.&npspchat<br/>
Volunteer&npsp15:&npsp9.&npspphone<br/>
Volunteer&npsp15:&npsp17.&npspphone<br/>
Volunteer&npsp16:&npsp2.&npspphone<br/>
Volunteer&npsp16:&npsp24.&npspphone<br/>
Volunteer&npsp17:&npsp6.&npspobserver<br/>
Volunteer&npsp17:&npsp14.&npspobserver<br/>
Volunteer&npsp17:&npsp19.&npspobserver<br/>
Volunteer&npsp17:&npsp26.&npspobserver</p>

<p>Remaining&npspcapacities:&npspNone</p>

<p>Day|&npspP&npsp&nbspC&npsp&nbspO<br/>
___|___________<br/>
&npsp1.|&npsp9&npsp&nbsp_<br/>
&npsp2.|&npsp16&npsp<br/>
&npsp3.|&npsp11&npsp&nbsp8<br/>
&npsp4.|&npsp12&npsp<br/>
&npsp5.|&npsp10&npsp<br/>
&npsp6.|&npsp2&npsp&nbsp&nbsp&nbsp17<br/>
&npsp7.|&npsp13&npsp<br/>
&npsp8.|&npsp6&nbsp11<br/>
&npsp9.|&npsp15&npsp<br/>
10.|&npsp9&nbsp14<br/>
11.|&npsp12&npsp<br/>
12.|&npsp2&npsp<br/>
13.|&npsp1&npsp<br/>
14.|&npsp8&nbsp17<br/>
15.|&npsp6&nbsp13<br/>
16.|&npsp10&npsp<br/>
17.|&npsp15&npsp_<br/>
18.|&npsp7&npsp<br/>
19.|&npsp4&npsp&nbsp&nbsp&nbsp17<br/>
20.|&npsp13&npsp<br/>
21.|&npsp9&npsp<br/>
22.|&npsp3&npsp&nbsp14<br/>
23.|&npsp2&npsp<br/>
24.|&npsp16&npsp&nbsp_<br/>
25.|&npsp5&npsp<br/>
26.|&npsp7&npsp&nbsp&nbsp17<br/>
27.|&npsp4&npsp<br/>
28.|&npsp2&npsp<br/>
29.|&npsp3&npsp&nbsp14<br/>
30.|&npsp1&npsp<br/>
</p>
