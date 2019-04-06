# https://github.com/imreszakal/helpline_scheduler

from ortools.sat.python import cp_model
import csv
import calendar
from _get_data import *
from _printout import *
from _arg_check import *

arg_check()

def main():
    # Get data from csv file
    get_data()

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # schedule[(v, d, s)]: volunteer 'v' works shift 's' on day 'd'.
    schedule = {}
    for v in volunteers:
        for d in list_of_days:
            for s in shifts:
                i = 'shift_{:_>2}.{:_>2}.{}'.format(v, d, s)
                schedule[(v, d, s)] = model.NewBoolVar(i)

    use_data()

    # Adding more constraints

    # Maximum one volunteer per shift.
    for d in list_of_days:
        # Phone shifts every day
        model.Add(sum(schedule[(v, d, 0)] for v in volunteers) <= 1)
        # Chat shifts on chat days
        if d in chat_days:
            model.Add(sum(schedule[(v, d, 1)] for v in volunteers) <= 1)
        # No chat shift for other days
        else:
            for v in volunteers:
                model.Add(schedule[(v, d, 1)] == False)
        # Plus shifts every day
        model.Add(sum(schedule[(v, d, 3)] for v in volunteers) <= 1)

    # At least four days between shifts per volunteer
    for v in volunteers:
        days = list_of_days
        for day in days:
            a = day-distance
            b = day+distance
            while a < 1:
                a += 1
            while b > days_in_month:
                b -= 1
            model.Add(sum(schedule[(v, d, s)]
                for s in shifts for d in range(a, b)) <= 1)

    # Observers only work with volunteers they are welcomed by
    for day in list_of_days:
        for o in observers:
            # Only if phone shift is filled
            model.Add(schedule[(o, d, 2)] <=
                sum(schedule[(v, d, 0)] for v in volunteers))
            for v in volunteers:
                # Only if welcomed by all other volunteers
                if v in welcomers:
                    model.Add(schedule[(o, d, 2)] <=
                        sum(schedule[(v, d, s)] for s in [0,1,3]))
                else:
                    for s in [0,1,3]:
                        model.Add((schedule[(o, d, 2)] and
                            schedule[(v, d, s)]) <= 1)

    # Cannot work alone
    for id in all_cannot_alone:
        days = [d for d in all_days_available[id]]
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
        days = [d for d in all_days_available[not_want[0]]]
        for d in days:
            model.Add(sum(schedule[(not_want[0], d, s)] for s in shifts)
                and sum(schedule[(v, d, s)]
                for v in them for s in shifts) == False)


    # OBJECTIVE

    # Filled phone shifts has the greatest priority
    model.Maximize(sum(
        100 * schedule[(v, d, 0)] + 50 * schedule[(v, d, 1)]
        + schedule[(v, d, 2)] +
        schedule[(v, d, 3)] if d in chat_days else 2 * schedule[(v, d, 3)]
        )
        for d in list_of_days for v in volunteers))


    # SOLUTION

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)

    printout()

if __name__ == '__main__':
    main()
