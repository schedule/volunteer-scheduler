# Helpline scheduling for a month
#
# Phone shift: every day of month
# Chat shift: Mondays and Wednesdays
#
# Constraints:
# Each volunteer gives a list of days they are available.
# Each volunteer has to have 4 days between their shifts.
# One volunteer only does chat because of hearing problems.
# Most volunteers only do phone because they are not qualified for chat.
# Some volunteers do both chat and phone.
#
# Priorities:
# 1.: Have minimum one volunteer for each day.
# 2.: Fill chat shifts.
# 3.: Have a second volunteer even on phone days.
#
# Possible options:
# - A certain amount of days of available days are only for weekends.
# - Does both chat and phone but prefers chat.
# - Wants to work alone.
# - Does not want to work with a certain volunteer.
# - Wants shifts on different weeks.
#
# Objective:
# Maximize filled shifts

input_list = []
def input(id, type, available, workload):
    input_list.append([id, type, available, workload])

# /////////////////////// BEGINNING OF INPUT /////////////////////////////
number_of_volunteers = 16
days_in_month = 30 # April 2019
first_monday = 1 # 1st of actual month is 1
distance = 2 # Distance between workdays per person
maximum_workload = 5

# input(Volunteer ID number, type, [days available])
# 'P':only phone  'C':only chat  'CP':chat and phone
input(1,'P',[2,4,9,11,13,16,25,30],2)
input(2,'CP',[4,6,8,9,11,12,14,15,18,19,20,21,22,23,25,26,28,29,30],4)
input(3,'CP',[8,15,20,22,23,25,29],2)
input(4,'P',[19,27],2)
input(5,'P',[25],1)
input(6,'P',[8,15],2)
input(7,'P',[5,18,19,26],2)
input(8,'CP',[3,14],2)
input(9,'P',[1,3,4,6,7,10,11,13,17,18,21,24,25,27,28],3)
input(10,'P',[5,16,19,26,29,30],2)
input(11,'CP',[1,2,3,4,5,8,9,10,11,12,15],2)
input(12,'P',[4,11,25],2)
input(13,'CP',[5,6,7,15,19,20,21,22,23,24],3)
input(14,'C',[10,22,24,29],3)
input(15,'P',[8,9,10,11,15,17,19,30],2)
input(16,'P',[1,2,3,4,5,24,25,26],2)

# ///////////////////////// END OF INPUT /////////////////////////////////

from ortools.sat.python import cp_model

def main():
    # Creates the model.
    model = cp_model.CpModel()

    # Volunteers ID list [1,2,3,...]
    volunteers = [i for i in range(1, number_of_volunteers + 1)]

    # Days' list [1,2,3,...]
    list_of_days = [i for i in range(1, days_in_month + 1)]

    # Chat days' list (Mondays and Wednesdays)
    chat_days = []
    m, w = first_monday, first_monday + 2
    # Mondays
    while m <= days_in_month:
        chat_days.append(m)
        m += 7
    # Wednesdays
    while w <= days_in_month:
        chat_days.append(w)
        w += 7

    # Weekend days (Saturdays and Sundays)
    weekend_days = []
    sat, sun = first_monday + 5, first_monday + 6
    # Mondays
    while sat <= days_in_month:
        weekend_days.append(sat)
        sat += 7
    # Wednesdays
    while sun <= days_in_month:
        weekend_days.append(sun)
        sun += 7

    # Separate lists for each week
    m = first_monday
    week_count = 0
    if m != 1:
        week_count +=1
    days = days_in_month
    while days > 0:
        week_count += 1
        days -= 7
    weeks = [list() for i in range(week_count)]
    week_index = 0
    d = 1
    while d <= days_in_month:
        while (d - m) / 7 < 1 and d <= days_in_month:
            weeks[week_index].append(d)
            d += 1
        week_index += 1
        m += 7

    # Phone: shift 0, Chat: shift 1
    shifts = [0,1]

    # Creates shift variables.
    # schedule[(v, d, s)]: volunteer 'v' works shift 's' on day 'd'.
    schedule = {}
    for v in volunteers:
        for d in list_of_days:
            for s in shifts:
                i = 'shift_{:_>2}.{:_>2}.{}'.format(v, d, s)
                schedule[(v, d, s)] = model.NewBoolVar(i)

    # Sets up class to processes input data
    class Vol:
        def __init__(self, id, type, days_available, workload):
            # Volunteers doing only chat
            if type == 'C':
                for d in list_of_days:
                    if d in days_available:
                        model.Add(schedule[(id, d, 1)] <= 1)
                    else:
                        model.Add(schedule[(id, d, 1)] <= 0)
                    model.Add(schedule[(id, d, 0)] <= 0)

            # Volunteers doing chat and phone
            if type == 'CP':
                for d in list_of_days:
                    for s in shifts:
                        if d in days_available:
                            model.Add(schedule[(id, d, s)] <= 1)
                        else:
                            model.Add(schedule[(id, d, s)] <= 0)

            # Volunteers doing only phone
            if type == 'P':
                for d in list_of_days:
                    if d in days_available:
                        model.Add(schedule[(id, d, 0)] <= 1)
                    else:
                        model.Add(schedule[(id, d, 0)] <= 0)
                    model.Add(schedule[(id, d, 1)] <= 0)

            # Workload
            model.Add(sum(schedule[(id, d, s)]
                for d in days_available for s in shifts) <= workload)

    # Puts input data into process
    for i in input_list:
        Vol(i[0], i[1], i[2], i[3])

    # Exactly one volunteer per shift.
    for d in list_of_days:
        # Phone shifts every day
        model.Add(sum(schedule[(v, d, 0)] for v in volunteers) == 1)
        # Chat shifts on chat days
        if d in chat_days:
            model.Add(sum(schedule[(v, d, 1)] for v in volunteers) <= 1)
        # No chat shift for other days
        else:
            model.Add(sum(schedule[(v, d, 1)] for v in volunteers) == 0)

    # At least four days between shifts per volunteer
    for v in volunteers:
        for day in list_of_days:
            a = day-distance
            b = day+distance+1
            while a < 1:
                a += 1
            while b > days_in_month:
                b -= 1
            model.Add(sum(schedule[(v, d, 0)] + schedule[(v, d, 1)]
                for d in range(a,b)) <= 1)


    # Special preferences of volunteers:

    # Maximum two weekends (Saturday, Sunday) for volunteer 2
    days = [d for d in weekend_days if d in input_list[1][2]]
    model.Add(sum(schedule[(2, d, s)] for d in days for s in shifts) <= 2)

    # Maximum one weekend for volunteer 9
    days = [d for d in weekend_days if d in input_list[8][2]]
    model.Add(sum(schedule[(9, d, 0)] for d in days) <= 1)

    # Volunteer 6 wants to work alone (No other volunteer on these days)
    days = [d for d in input_list[5][2]]
    for d in days:
        model.Add(schedule[(6, d, 0)] + schedule[(6, d, 1)] <= 1)

    # Volunteer 9 wants shifts to be on different weeks
    days = [d for d in input_list[8][2]]
    for week in weeks:
        model.Add(sum(schedule[(9, d, 0)] for d in week if d in days) <= 1)


    # OBJECTIVE
    model.Maximize(sum(schedule[(v, d, s)]
            for d in list_of_days for s in shifts for v in volunteers))


    # SOLUTION

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)

    # Prints out workload for each volunteer
    print()
    print('2019 April   -   Distance: ' + str(distance))
    print()
    for v in volunteers:
        for d in list_of_days:
            for s in shifts:
                if solver.Value(schedule[(v, d, s)]) == 1:
                    if s == 0:
                        t = 'phone'
                    else:
                        t = 'chat'
                    print('Volunteer {}: {}. {}'.format(v,d,t))
    print()

    # Who works less than willing?
    print('Remaining capacities: ', end='')
    free_capacity = False
    for v in volunteers:
        works = 0
        for d in list_of_days:
            for s in shifts:
                if solver.Value(schedule[(v, d, s)]) == 1:
                    works += 1
        more = input_list[v-1][3] - works
        if more > 0:
            free_capacity = True
            more = input_list[v-1][3] - works
            print('Free capacity of volunteer {}: {} day'\
                .format(v, more), end='')
            if more > 1:
                print('s.')
            else:
                print('.')
    if not free_capacity:
        print('None')
    print()

    print('Day|  P  C')
    print('___|________')
    for d in list_of_days:
        phone, chat = 0, 0
        print('{:>2}.| '.format(d), end='')

        # Phone
        for v in volunteers:
            if solver.Value(schedule[(v, d, 0)]) == 1:
                phone = v
                break
        if phone:
            print('{:>2} '.format(v), end='')
        else:
            print(' _ ', end='')

        # Chat
        for v in volunteers:
            if solver.Value(schedule[(v, d, 1)]) == 1:
                chat = v
                break
        if chat:
            print('{:>2} '.format(v), end='')
        elif d in chat_days:
            print(' _ ', end='')
        print()
    print()
    print()
    print()

if __name__ == '__main__':
    main()
