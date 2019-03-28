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
# Operator or Hospiter: Hospiter is second or third.
# Operator option: welcomes hospiter or not.
# Hospiter also gives available days
#
# Priorities:
# 1.: Have minimum one volunteer for each day.
# 2.: Fill chat shifts.
# 3.: Have a second volunteer even on phone days.
#
# Possible options:
# - A certain amount of days of available days are only for weekends.
# - Does both chat and phone but prefers chat.
# - Welcomes observer volunteer to work on the same day.
# - Does not want to work with a certain volunteer.
# - Wants their shifts to be on separate weeks.
# - Wants to work alone.
# - Cannot work alone.
# - Do not want to work with some other people.
#
# Objective:
# Maximize filled shifts

input_list = []
def input(id, type, days_available, workload, max_weekend_days,
        welcomes_observer, separate_w, alone, cannot_alone, not_with):
    input_list.append([id, type, days_available, workload, max_weekend_days,
        welcomes_observer, separate_w, alone, cannot_alone, not_with])

# /////////////////////// BEGINNING OF INPUT /////////////////////////////
number_of_volunteers = 17
days_in_month = 30 # April 2019
first_monday = 1 # 1st of actual month is 1
distance = 2 # Distance between workdays per person

# input(
# 1: Volunteer ID number,
# 2: type, ('P':only phone  'C':only chat  'CP':chat and phone  'O':observer)
# 3: [days available],
# 4: maximum total workload
# 5: max weekend days,
# 6: welcomes observer,
# 7: wants shifts to be on separate weekends,
# 8: wants to work alone,
# 9: cannot work alone),
# 10: does not want to work with
#
input(1,'P',[2,4,9,11,13,16,25,30],2,2,True,False,False,False,[])
input(2,'CP',[4,6,8,9,11,12,14,15,18,19,20,21,22,23,25,26,28,29,30],4,2,False,False,False,False,[])
input(3,'CP',[8,15,20,22,23,25,29],2,2,True,False,False,False,[])
input(4,'P',[19,27],2,2,True,False,False,False,[])
input(5,'P',[25],1,1,True,False,False,False,[])
input(6,'P',[8,15],2,2,True,False,False,True,[])
input(7,'P',[5,18,19,26],2,2,True,False,False,False,[])
input(8,'CP',[3,14],2,2,True,False,False,False,[])
input(9,'P',[1,3,4,6,7,10,11,13,17,18,21,24,25,27,28],3,1,False,False,False,False,[])
input(10,'P',[5,16,19,26,29,30],2,2,False,False,False,False,[])
input(11,'CP',[1,2,3,4,5,8,9,10,11,12,15],2,2,False,False,False,False,[8])
input(12,'P',[4,11,25],2,2,False,False,False,False,[])
input(13,'CP',[5,6,7,15,19,20,21,22,23,24],3,3,False,False,False,False,[])
input(14,'C',[10,22,24,29],3,3,False,False,False,False,[])
input(15,'P',[8,9,10,11,15,17,19,30],2,2,False,False,False,False,[])
input(16,'P',[1,2,3,4,5,24,25,26],2,2,False,False,False,False,[])
# Observer
input(17,'O',[4,6,8,9,11,12,14,15,18,19,20,21,22,23,25,26,28,29,30],4,2,False,False,False,False,[])


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

    # Phone: shift 0, Chat: shift 1, Observation: shift 2
    shifts = [0,1,2]

    # List of volunteers welcoming observers and list of observers:
    welcomers = []
    observers = []

    # List of volunteers who cannot work alone
    cannot_work_alone = []

    # List of volunteer who does not want to work with someone
    not_with_them = []

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
        def __init__(self, id, type, days_available, workload,
            max_weekend_days, welcomes_observer, separate_w, alone,
            cannot_alone, not_with):
            # Volunteers doing only chat
            if type == 'C':
                for d in list_of_days:
                    for s in [0,2]:
                        model.Add(schedule[(id, d, s)] == 0)
                    if d in days_available:
                        model.Add(schedule[(id, d, 1)] <= 1)
                    else:
                        model.Add(schedule[(id, d, 1)] == 0)

            # Volunteers doing chat and phone
            if type == 'CP':
                for d in list_of_days:
                    model.Add(schedule[(id, d, 2)] == 0)
                    if d in days_available:
                        for s in [0,1]:
                            model.Add(schedule[(id, d, s)] <= 1)
                    else:
                        for s in [0,1]:
                            model.Add(schedule[(id, d, s)] == 0)

            # Volunteers doing only phone
            if type == 'P':
                for d in list_of_days:
                    for s in [1,2]:
                        model.Add(schedule[(id, d, s)] == 0)
                    if d in days_available:
                        model.Add(schedule[(id, d, 0)] <= 1)
                    else:
                        model.Add(schedule[(id, d, 0)] == 0)

            # Volunteers doing observation
            if type == 'O':
                observers.append(id)
                for d in list_of_days:
                    for s in [0,1]:
                        model.Add(schedule[(id, d, s)] == 0)
                    if d in days_available:
                        model.Add(schedule[(id, d, 2)] <= 1)
                    else:
                        model.Add(schedule[(id, d, 2)] == 0)

            # List observers and volunteers welcoming observers
            if type in ['C', 'CP', 'P'] and welcomes_observer:
                welcomers.append(id)

            # Total workload
            model.Add(sum(schedule[(id, d, s)]
                for d in days_available for s in shifts) <= workload)

            # Max weekend days
            max_weekend_days
            days = [d for d in weekend_days if d in days_available]
            model.Add(sum(schedule[(id, d, s)]
                for d in days for s in shifts) <= max_weekend_days)

            # Wants shifts to be on different weeks
            if separate_w:
                for week in weeks:
                    model.Add(sum(schedule[(id, d, s)]
                        for s in shifts for d in week
                        if d in days_available) <= 1)

            # Wants to work alone
            if alone:
                days = [d for d in days_available]
                others = [i for i in volunteers if i != id]
                for d in days:
                    model.Add(sum(schedule[(v, d, s)] for v in others
                        for s in shifts) + schedule[(id, d, s)] <= 1)

            # Cannot work alone
            if cannot_alone:
                cannot_work_alone.append(id)

            # Does not want to work with XY
            if not_with:
                not_with_them.append([id, not_with])



    # Puts input data into process
    for i in input_list:
        Vol(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9])

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
            model.Add(sum(schedule[(v, d, s)]
                for s in shifts for d in range(a,b)) <= 1)

    # Observers only work with volunteers they are welcomed by
    for day in list_of_days:
        for o in observers:
            for v in volunteers:
                for s in [0,1]:
                    if v in welcomers:
                        model.Add(schedule[(o, d, 2)] <=
                            schedule[(v, d, s)])
                    else:
                        model.Add(schedule[(o, d, 2)] and
                            schedule[(v, d, s)] == False)

    # Cannot work alone
    for id in cannot_work_alone:
        days = [d for d in input_list[id-1][2]]
        others = [i for i in volunteers if i != id
            and i not in cannot_work_alone]
        other_not_alones = [i for i in cannot_work_alone if i != id]
        for d in days:
            # Only can work on a day when other volunteer works who
            # can work alone
            model.Add(sum(schedule[(id, d, s)] for s in shifts) <=
                sum(schedule[(v, d, s)]
                for v in others for s in shifts))
            # Cannot work on the same day as other volunteer who
            # cannot work alone
            model.Add(sum(schedule[(id, d, s)] for s in shifts) and
                sum(schedule[(v, d, s)]
                for v in other_not_alones for s in shifts) == False)

    # Does not want to work with XY
    for not_want in not_with_them:
        them = not_want[1]
        for d in days:
            model.Add(sum(schedule[(not_want[0], d, s)] for s in shifts)
                and sum(schedule[(v, d, s)]
                for v in them for s in shifts) == False)

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
                    elif s == 1:
                        t = 'chat'
                    elif s == 2:
                        t = 'observer'
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

    print('Day|  P  C  O')
    print('___|___________')
    for d in list_of_days:
        phone, chat, observer = False, False, False
        print('{:>2}.| '.format(d), end='')

        # Phone
        for v in volunteers:
            if solver.Value(schedule[(v, d, 0)]) == 1:
                phone = True
                break
        if phone:
            print('{:>2} '.format(v), end='')
        else:
            print(' _ ', end='')

        # Chat
        for v in volunteers:
            if solver.Value(schedule[(v, d, 1)]) == 1:
                chat = True
                break
        if chat:
            print('{:>2} '.format(v), end='')
        elif d in chat_days:
            print(' _ ', end='')
        else:
            print('   ', end='')

        # Observer
        for v in volunteers:
            if solver.Value(schedule[(v, d, 2)]) == 1:
                observer = True
                break
        if observer:
            print('{:>2} '.format(v), end='')
        print()
    print()
    print()
    print()

if __name__ == '__main__':
    main()
