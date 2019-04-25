# https://github.com/imreszakal/volunteer-scheduler

from ortools.sat.python import cp_model
import calendar
import csv
import sys
import os
import datetime
import config

language = config.language
if language == 'EN':
   from lang.language_EN import *
elif language == 'HU':
   from lang.language_HU import *
elif language == 'CN':
   from lang.language_CN import *
else:
    print('You need to set language in config.py.')

def main():
    f = []
    with open(l_filename, encoding='UTF8') as data_file:
         reader = csv.reader(data_file, delimiter=',')
         for row in reader:
             f.append(row)
    schedule_year = int(f[0][1])
    schedule_month = int(f[1][1])
    month_name = l_month_name_dic[schedule_month]
    data_lines = []
    for line in range(5, len(f)):
        if f[line][3]:
            data_lines.append(line)

    number_of_volunteers = len(data_lines)
    volunteers = [i for i in range(number_of_volunteers)]

    firstday_index, days_in_month = calendar.monthrange(schedule_year,
            schedule_month)

    list_of_days = [i for i in range(1, days_in_month + 1)]

    if firstday_index == 0:
        first_monday = 1
    else:
        first_monday = 8 - firstday_index



    weeks = {}
    m = firstday_index
    week_index = 0
    d = 1
    what_day_dic = {}
    while d <= days_in_month:
        weeks[week_index] = list()
        while d + m - week_index * 7 < 8 and d <= days_in_month:
            weeks[week_index].append(d)
            what_day_dic[d] = d + m - week_index * 7
            d += 1
        week_index += 1

    def certain_weekdays_in_month(list_of_certain_weekdays): # Monday: 1
        days = []
        for c in list_of_certain_weekdays:
            for d in list_of_days:
                if what_day_dic[d] == c:
                    days.append(d)
        return days

    chat_days = certain_weekdays_in_month([1, 3])
    weekend_days = certain_weekdays_in_month([6, 7])
    not_chat_days = [d for d in list_of_days if d not in chat_days]

    # Distance between workdays per person
    distance = 2

    # Phone: shift 0, Chat: shift 1, Observation: shift 2,
    # Remainder: shift 3
    shifts = [0, 1, 2, 3]

    model = cp_model.CpModel()

    # Creates shift variables.
    # schedule[(v, d, s)]: volunteer 'v' works shift 's' on day 'd'.
    schedule = {}
    for v in volunteers:
        for d in list_of_days:
            for s in shifts:
                i = 'shift_{:_>2}.{:_>2}.{}'.format(v, d, s)
                schedule[(v, d, s)] = model.NewBoolVar(i)

    all_days_available = []
    all_workload = []
    all_wants_alone = []
    all_cannot_alone = []
    all_not_with = []
    welcomers = []
    observers = []
    cannot_work_alone = []
    not_with_them = []

    def use_data(id, type, days_available, workload,
            max_weekend_days, welcomes_observer, separate_w, alone,
            cannot_alone, not_with):

        all_days_available.append(days_available)
        all_workload.append(workload)

        # Volunteers doing only chat
        if type == l_C:
            for d in list_of_days:
                for s in [0, 2, 3]:
                    model.Add(schedule[(id, d, s)] == False)
                if d in days_available:
                    model.Add(schedule[(id, d, 1)] <= 1)
                else:
                    model.Add(schedule[(id, d, 1)] == False)

        # Volunteers doing chat and phone
        if type == l_CP:
         for d in list_of_days:
             model.Add(schedule[(id, d, 2)] == False)
             if d in days_available:
                 model.Add(sum(schedule[(id, d, s)] for s in [0, 1, 3]) <= 1)
             else:
                 for s in [0, 1, 3]:
                     model.Add(schedule[(id, d, s)] == False)

        # Volunteers doing only phone
        if type == l_P:
            for d in list_of_days:
                for s in [1, 2]:
                    model.Add(schedule[(id, d, s)] == False)
                if d in days_available:
                    model.Add(sum(schedule[(id, d, s)]
                         for s in [0, 3]) <= 1)
                else:
                    for s in [0,3]:
                        model.Add(schedule[(id, d, s)] == False)

        # Volunteers doing observation
        if type == l_O:
            observers.append(id)
            for d in list_of_days:
                for s in [0, 1, 3]:
                    model.Add(schedule[(id, d, s)] == False)
                if d in days_available:
                    model.Add(schedule[(id, d, 2)] <= 1)
                else:
                    model.Add(schedule[(id, d, 2)] == False)

        # Total workload
        model.Add(sum(schedule[(id, d, s)]
                for d in days_available for s in shifts) <= workload)

        # Max weekend days
        max_weekend_days
        days = [d for d in weekend_days if d in days_available]
        model.Add(sum(schedule[(id, d, s)]
                for d in days for s in shifts) <= max_weekend_days)

        # List observers and volunteers welcoming observers
        if type in [l_C, l_CP, l_P] and welcomes_observer:
            welcomers.append(id)

        # Wants shifts to be on different weeks
        if separate_w:
            for i in weeks:
                model.Add(sum(schedule[(id, d, s)] for s in shifts
                        for d in weeks[i] if d in days_available) <= 1)

        # Wants to work alone
        if alone:
            all_wants_alone.append(id)

        # Cannot work alone
        if cannot_alone:
            all_cannot_alone.append(id)

        # Does not want to work with XY
        if not_with:
            not_with_them.append([id, not_with])

    # volunteer_dic = {ID:name}, volunteer_dic_r = {name:ID}
    volunteer_dic = {}
    volunteer_dic_r = {}
    id = 0
    for line in data_lines:
        volunteer_dic[id] = f[line][1]
        volunteer_dic_r[f[line][1]] = id
        id += 1

    def bool_from_string(value):
        if value == '1':
            return True
        else:
            return False

    # Loads data
    id = 0
    for line in data_lines:
         values = [x for x in f[line]]
         type = values[2]

         days_available = [int(x) for x in values[3].split(',')
                if x.strip().isdigit()]

         workload = int(values[4])
         max_weekend_days = int(values[5])

         welcomes_observer = bool_from_string(values[6])
         separate_w = bool_from_string(values[7])
         alone = bool_from_string(values[8])
         cannot_alone = bool_from_string(values[9])

         not_with = [volunteer_dic_r[name] for name in values[10].split(',')
                if name]

         use_data(id, type, days_available, workload, max_weekend_days,
                welcomes_observer, separate_w, alone, cannot_alone, not_with)
         id += 1

    # Maximum one volunteer per shift.
    for d in list_of_days:
        # Phone shifts every day
        model.Add(sum(schedule[(v, d, 0)] for v in volunteers) <= 1)
        # Plus shifts every day
        model.Add(sum(schedule[(v, d, 3)] for v in volunteers) <= 1)
        # Chat shifts on chat days
        if d in chat_days:
            model.Add(sum(schedule[(v, d, 1)] for v in volunteers) <= 1)
        # No chat shift for other days
        else:
            for v in volunteers:
                model.Add(schedule[(v, d, 1)] == False)

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
                    for s in shifts for d in range(a, b + 1)) <= 1)

    # Observers only work with volunteers they are welcomed by
    for d in list_of_days:
        for o in observers:
            for v in volunteers:
                if v not in welcomers:
                    for s in [0, 1, 3]:
                        model.Add(schedule[(o, d, 2)] + schedule[(v, d, s)] <=1)

    # Cannot work alone
    for id in all_cannot_alone:
        days = [d for d in all_days_available[id]]
        others = [i for i in volunteers if i != id
                and i not in all_cannot_alone]
        other_not_alones = [i for i in all_cannot_alone if i != id]
        for d in days:
            # Only can work on a day when other volunteer works who
            # can work alone
            model.Add(sum(schedule[(id, d, s)] for s in shifts)
                    <= sum(schedule[(v, d, s)] for v in others for s in shifts))
            # Cannot work on the same day as other volunteer who
            # cannot work alone
            model.Add(sum(schedule[(id, d, s)] for s in shifts)
                    and sum(schedule[(v, d, s)]
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
    model.Maximize(
            sum(schedule[(v, d, 0)] * 11 for d in chat_days
                    for v in volunteers)
            + sum(schedule[(v, d, 0)] * 10 for d in not_chat_days
                    for v in volunteers)
            + sum(schedule[(v, d, 1)] * 9
                    + schedule[(v, d, 2)]
                    for d in list_of_days for v in volunteers)
            + sum(schedule[(v, d, 3)] * 7 for d in chat_days
                    for v in volunteers)
            + sum(schedule[(v, d, 3)] * 8 for d in not_chat_days
                    for v in volunteers)
            - sum(schedule[(wa, d, 0)] and schedule[(v, d, s)]
                    for s in [1,2,3] for v in volunteers
                    for wa in all_wants_alone for d in list_of_days)
            - sum(schedule[(wa, d, 1)] and schedule[(v, d, s)]
                    for s in [0,2,3] for v in volunteers
                    for wa in all_wants_alone for d in list_of_days)
            - sum(schedule[(wa, d, 2)] and schedule[(v, d, s)]
                    for s in [0,1,3] for v in volunteers
                    for wa in all_wants_alone for d in list_of_days)
            - sum(schedule[(wa, d, 3)] and schedule[(v, d, s)]
                    for s in [0,1,2] for v in volunteers
                    for wa in all_wants_alone for d in list_of_days)
    )

    # SOLUTION

    solver = cp_model.CpSolver()
    solver.Solve(model)

    solution_vs_d = {}
    for s in shifts:
        for v in volunteers:
            has = False
            for d in list_of_days:
                if solver.Value(schedule[(v, d, s)]) == 1:
                    if has:
                        solution_vs_d[(v, s)].append(d)
                    else:
                        solution_vs_d[(v, s)] = list()
                        solution_vs_d[(v, s)].append(d)
                    has = True

    solution_v_phonedays = {}
    for v in volunteers:
        tel1 = []
        tel2 = []
        try:
            tel1 = solution_vs_d[(v, 0)]
        except:
            pass
        try:
            tel2 = solution_vs_d[(v, 3)]
        except:
            pass
        solution_v_phonedays[v] = tel1 + tel2

    solution_ds_v = {}
    for v in volunteers:
        for s in shifts:
            try:
                days = solution_vs_d[(v, s)]
                for day in days:
                    solution_ds_v[(day, s)] = v
            except:
                pass

    solution_vd_s = {}
    for v in volunteers:
        for day in list_of_days:
            try:
                if day in solution_v_phonedays[v]:
                    solution_vd_s[(v, day)] = 0
            except:
                pass
            for s in [1, 2]:
                try:
                    if solution_ds_v[(day, s)] == v:
                        solution_vd_s[(v, day)] = s
                except:
                    pass

    needed = {}
    needed[0] = []
    for d in list_of_days:
        try:
            a = solution_ds_v[(d, 0)]
        except:
            print('T', d)
            needed[0].append(d)
    needed[1] = []
    for d in chat_days:
        try:
            a = solution_ds_v[(d, 1)]
        except:
            print('C', d)
            needed[1].append(d)

    if not os.path.exists('output'):
        os.makedirs('output')

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = 'output/{}_{}_{}____{}'.format(l_output_filename,
            schedule_year, schedule_month, timestamp)
    txt_file = new_filename + '.txt'
    csv_file = new_filename + '.csv'

    global width
    width = 18 #     minimum 14

    def print_txt(*txt_line):
        try:
            w = txt_line[0]
            print(w)
        except:
            w = '\n'
            print()
        with open(txt_file, 'a', encoding='UTF8') as f:
            f.write(w + '\n')

    def csv_cell(cell_data):
        c = ''
        if cell_data:
            try:
                # number
                if cell_data[0] > 0:
                    if len(cell_data) > 1:
                        c += '"' + str(cell_data[0])
                        for j in cell_data[1:]:
                            c += ',' + str(j)
                        c += '"'
                    else:
                        c += str(cell_data[0])
            except:
                # string
                c = str(cell_data)
        return c

    def print_days(list):
        t = ''
        if list:
            if len(list) > 1:
                t += str(list)
                for j in list[1:]:
                    t += '.,' + str(j)
            else:
                t += str(list[0]) + '.'
        return t

    def print_csv(list):
        line = ''
        line = ','.join(csv_cell(i) for i in list)
        with open(csv_file, 'a', encoding='UTF8') as f:
            f.write(line + ',\n')

    def calendar_solution(d, l_X, shift, everyday, chatday):
        txt_item = ''
        csv_item = ''
        title = l_X + ': '
        try:
            v = solution_ds_v[(d, shift)]
            txt_item = title + vol_l[v] + ' ' * 2
            csv_item = title + volunteer_dic[v]
        except:
            if everyday or chatday and d in chat_days:
                csv_item = title + '-'
                txt_item = title + '-' + ' ' * (width - 4)
            else:
                csv_item = ''
                txt_item = ' ' * width
        return txt_item, csv_item

    def daily_txt_solution(day, shift, everyday, chatday):
        has = False
        daily_shift_item = ''
        try:
            v = solution_ds_v[(day, shift)]
            has = True
        except:
            pass
        if has:
            daily_shift_item += ' ' * 5 + vol_r[v]
        elif everyday or chatday and day in chat_days:
            daily_shift_item += ' ' * (width - 6) + ' ' * 5 + '-'
        else:
            daily_shift_item += ' ' * width
        return daily_shift_item

    vol_l = {}
    vol_r = {}
    w = width - 5
    for v in volunteers:
        if ord(volunteer_dic[v][0]) < 1000:
            vol_l[v] = volunteer_dic[v].ljust(w)
            vol_r[v] = volunteer_dic[v].rjust(w)
        else:
            length = len(volunteer_dic[v])
            if length in [1, 2, 3]:
                alignment_shift = length
            if length == 4:
                alignment_shift = 3
            if length == 5:
                alignment_shift = 1
            e = l_encoding
            vol_l[v] = volunteer_dic[v].encode(e).ljust(w).decode(e)
            vol_l[v] +=  ' ' * alignment_shift
            vol_r[v] = volunteer_dic[v].encode(e).rjust(w).decode(e)
            vol_r[v] = ' ' * alignment_shift + vol_r[v]

    def horizontal_line():
        print_txt('_' * 7 * width)


    # Calendar
    # TXT and CSV

    print_txt()
    print_txt()
    print_txt(str(schedule_year) + ' ' + month_name)
    print_txt()
    print_txt()
    print_csv([schedule_year, month_name])
    print_csv([])

    txt_weekday_line = ''
    for weekday in l_weekday_name_list:
        txt_weekday_line += '{:<{}}'.format(weekday, width)
    print_txt(txt_weekday_line)
    csv_weekday_line = ['']
    csv_weekday_line.extend([weekday for weekday in l_weekday_name_list])
    print_csv(csv_weekday_line)
    txt_1st_calendar_w_aligner = ' ' * width * firstday_index
    csv_1st_calendar_w_aligner = ',' * firstday_index
    txt_lines = [list() for i in range(5)]
    csv_lines = [list() for i in range(5)]
    for i in weeks:
        horizontal_line()

        for j in range(5):
            txt_lines[j] = ''
        for j in range(5):
            csv_lines[j] = ['']

        if txt_1st_calendar_w_aligner:
            for k in range(5):
                txt_lines[k] = txt_1st_calendar_w_aligner
            txt_1st_calendar_w_aligner = False
        if csv_1st_calendar_w_aligner:
            for k in range(5):
                csv_lines[k].extend(['' for i in csv_1st_calendar_w_aligner])
            csv_1st_calendar_w_aligner = False

        for d in weeks[i]:
            txt_lines[0] += '{:<{}}'.format(d, width)
            csv_lines[0].append(d)

            txt_item, csv_item = calendar_solution(d, l_P, 0, True, False)
            txt_lines[1] += txt_item
            csv_lines[1].append(csv_item)

            txt_item, csv_item = calendar_solution(d, l_E, 3, False, False)
            txt_lines[2] += txt_item
            csv_lines[2].append(csv_item)

            txt_item, csv_item = calendar_solution(d, l_C, 1, False, True)
            txt_lines[3] += txt_item
            csv_lines[3].append(csv_item)

            txt_item, csv_item = calendar_solution(d, l_O, 2, False, False)
            txt_lines[4] += txt_item
            csv_lines[4].append(csv_item)

        for line in txt_lines:
            print_txt(line)
        print_txt()
        print_txt()

        for line in csv_lines:
            print_csv(line)
        print_csv([])

    horizontal_line()
    print_txt()
    print_txt()
    print_txt()
    print_txt()
    print_csv([])


    # By day
    # TXT only
    w = width
    if ord(l_Day[-1]) < 1000:
        print_txt('{:>9}|{:>{}}{:>{}}{:>{}}{:>{}}'.format(l_Day, l_Phone, w,
                l_Extra, w, l_Chat, w, l_Observer, w))
    else:
        print_txt(l_Day + '|' + l_Phone + l_Extra + l_Chat + l_Observer)
    print_txt('_' * 9 + '|' + '_' * 4 * w)

    for d in list_of_days:
         line = ''
         phone, chat, observer, extra = False, False, False, False
         line += '{:>8}.|'.format(d)

         line += daily_txt_solution(d, 0, True, False)
         line += daily_txt_solution(d, 3, False, False)
         line += daily_txt_solution(d, 1, False, True)
         line += daily_txt_solution(d, 2, False, False)

         print_txt(line)
    print_txt()
    print_txt()


    # By volunteer
    # TXT
    shift_dic = {0:l_phone, 1:l_chat, 2:l_observer, 3:l_extra}
    for v in volunteers:
        has = False
        for day in all_days_available[v]:
            for s in [0, 1, 2]:
                try:
                    if s == solution_vd_s[(v, day)]:
                        shift_name = shift_dic[s]
                        text = ''
                        if has:
                            text = ' ' * (width - 5) + ' '
                        else:
                            text = vol_r[v] + ':'
                        weekday = l_weekday_name_list[what_day_dic[day]-1]
                        print_txt(text + ' {:>2}. {}, {}'.format(day,
                                weekday.lower(), shift_name))
                        has = True
                except:
                    pass
        if has:
            print_txt()
    print_txt()

    # CSV
    print_csv(['', l_Name, l_Phone, l_Chat, l_Observer])
    for v in volunteers:
        line = ['']
        line.append(volunteer_dic[v])
        try:
            line.append(csv_cell(solution_v_phonedays[v]))
        except:
            line.append('')
        for s in [1, 2]:
            try:
                line.append(csv_cell(solution_vs_d[(v, s)]))
            except:
                line.append('')
        print_csv(line)


    # Capacities
    # TXT only
    print_txt(l_workloads + ': ')
    nonzero_capacity = False
    for v in volunteers:
        line = ''
        works = 0
        more = 0
        workload = all_workload[v]
        for s in shifts:
            try:
                works += len(solution_vs_d[(v, s)])
            except:
                pass
        more = workload - works
        if more > 0 or more < 0:
            name = volunteer_dic[v]
            nonzero_capacity = True
            line += '    {:>10} '.format(name)
            if l_works_a:
                line += l_works_a + ' '
            line += str(works) + ' ' + l_day_maybe_plural(works)
            if l_works_b:
                line += ' ' + l_works_b
            line += ', '
            if l_but_offered_a:
                line += l_but_offered_a + ' '
            line += str(workload) + ' ' + l_day_maybe_plural(workload)
            if l_but_offered_b:
                line += ' ' + l_but_offered_b
            line += '.'
            print_txt(line)
            print_txt()
    if not nonzero_capacity:
        print_txt(l_capacity + '.')
    print_txt()

    # Needed
    if needed[0] or needed[1]:
        print_txt(l_need)
        if needed[0]:
            print_txt(' ' * 10 + l_Phone + ': ' + print_days(needed[0]))
        if needed[1]:
            print_txt(' ' * 10 + l_Chat + ': ' + print_days(needed[1]))
    print_txt()
    print_txt()

    print(l_created, txt_file)
    print(l_created, csv_file)
    print_txt()
    print_txt()
    print_txt()

    if l_message_1:
        print_txt(' ' * 10 + l_message_1)
        print_txt(' ' * 36 + l_message_2)
        print_txt()
    print_txt()
    print_txt(' ' * 10 + 'Copyright (c) 2019, Imre Szakal (imreszakal.com)')
    print_txt()

if __name__ == '__main__':
    main()
