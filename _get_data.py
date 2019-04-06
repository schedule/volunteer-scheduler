def get_data():
    f = []
    with open(filename, encoding='UTF8') as csvfile:
         reader = csv.reader(csvfile, delimiter=',')
         for row in reader:
             f.append(row)
    schedule_year = int(f[0][1])
    schedule_month = int(f[1][1])
    month_name = month_name_dic[schedule_month]
    data_lines = []
    for line in range(5, len(f)):
        if f[line][3]:
            data_lines.append(line)

    number_of_volunteers = len(data_lines)
    # Volunteers ID list [0,1,2,3,...]
    volunteers = [i for i in range(number_of_volunteers)]

    # Days in month; firstday 0 if monday
    firstday, days_in_month = calendar.monthrange(schedule_year,
                                                   schedule_month)

    # Days' list [1,2,3,...]
    list_of_days = [i for i in range(1, days_in_month + 1)]
    # First Monday of the month

    if firstday == 0:
        first_monday = 1
    else:
        first_monday = 8 - firstday

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

    # weeks dictionary
    weeks = {}
    m = firstday
    week_index = 0
    d = 1
    while d <= days_in_month:
        weeks[week_index + 1] = list()
        while d + m - week_index * 7 < 8 and d <= days_in_month:
            weeks[week_index + 1].append(d)
            d += 1
        week_index += 1
    week_count = len(weeks)
    week_indexes = [i + 1 for i in range(week_count)]

    # Distance between workdays per person
    distance = 2

    # Phone: shift 0, Chat: shift 1, Observation: shift 2,
    # Remainder: shift 3
    shifts = [0,1,2,3]
