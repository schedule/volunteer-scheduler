def printout():
    vol_l = {}
    vol_r = {}
    for v in volunteers:
         width = 11
         if ord(volunteer_dic[v][0]) < 1000:
             vol_l[v] = volunteer_dic[v].ljust(width)
             vol_r[v] = volunteer_dic[v].rjust(width)
         else:
             vol_l[v] = volunteer_dic[v].encode(encoding).ljust(width).decode(encoding)
             # while len(vol_l[v]) < width:
                 # vol_l[v] += ' '
             vol_r[v] = volunteer_dic[v].encode(encoding).rjust(width).decode(encoding)
             # while len(vol_l[v]) < width:
                 # vol_l[v] = ' ' + vol_l[v]
    # kinai: XXX: -3, XX: -2, X: -1

    print()
    def horizontal_line():
         print('_' * 108)

    def write_l(name, width):
         if ord(volunteer_dic[v][0]) < 1000:
             return name.ljust(width)
         else:
             return name.encode(encoding).ljust(width).decode(encoding)

    def write_r(name, width):
         if ord(volunteer_dic[v][0]) < 1000:
             return name.rjust(width)
         else:
             return name.encode(encoding).rjust(width).decode(encoding)

    first_shift = ''
    print()
    print()
    print(str(schedule_year) + after_year + ' ' + month_name)
    first_shift = ' ' * 16 * firstday

    for i in week_indexes:
         horizontal_line()
         line_0 = ''
         line_1 = ''
         line_2 = ''
         line_3 = ''
         line_4 = ''
         if first_shift:
             line_0 += first_shift
             line_1 += first_shift
             line_2 += first_shift
             line_3 += first_shift
             line_4 += first_shift
             first_shift = 0

         for d in weeks[i]:
             phone, chat, observer, extra = False, False, False, False
             line_0 += '{:<2}'.format(d) + ' ' * 14

             # Phone
             for v in volunteers:
                 if solver.Value(schedule[(v, d, 0)]) == 1:
                     phone = True
                     break
             if phone:
                 line_1 += l_P + ': ' + vol_l[v] + ' ' * 2
             else:
                 line_1 += l_P + ': -' + ' ' * 12

             # Chat
             for v in volunteers:
                 if solver.Value(schedule[(v, d, 1)]) == 1:
                     chat = True
                     break
             if chat:
                 line_2 += l_C + ': ' + vol_l[v] + ' ' * 2
             elif d in chat_days:
                 line_2 += l_C + ': -' + ' ' * 12
             else:
                 line_2 += ' ' * 16

             # Observer
             for v in volunteers:
                 if solver.Value(schedule[(v, d, 2)]) == 1:
                     observer = True
                     break
             if observer:
                 line_3 += l_O + ': ' + vol_l[v] + ' ' * 2
             else:
                 line_3 += ' ' * 16

             # Extra
             for v in volunteers:
                 if solver.Value(schedule[(v, d, 3)]) == 1:
                     extra = True
                     break
             if extra:
                 line_4 += l_E + ': ' + vol_l[v] + ' ' * 2
             else:
                 line_4 += ' ' * 16
         print(line_0)
         print(line_1)
         print(line_2)
         print(line_3)
         print(line_4)
    horizontal_line()
    print()
    print()
    print()


    # print(str(schedule_year) + ' ' + month_name)
    if ord(l_Day[-1]) < 1000:
         print('{:>9}|{:>11}{:>11}{:>11}{:>11}'.format(l_Day,
                                 l_Phone, l_Chat, l_Observer, l_Extra))
    else:
         print(l_Day + '|' + l_Phone, l_Chat, l_Observer, l_Extra)
    print('_' * 9 + '|' + '_' * 48)

    for d in list_of_days:
         line = ''
         phone, chat, observer, plus = False, False, False, False
         line += '{:>8}.|'.format(d)

         # Phone
         for v in volunteers:
             if solver.Value(schedule[(v, d, 0)]) == 1:
                 phone = True
                 break
         if phone:
             line += vol_r[v]
         else:
             line += write_r('      _    ', 11)

         # Chat
         for v in volunteers:
             if solver.Value(schedule[(v, d, 1)]) == 1:
                 chat = True
                 break
         if chat:
             line += vol_r[v]
         elif d in chat_days:
             line += write_r('      _    ', 11)
         else:
             line += write_r(' ' * 11, 11)

         # Observer
         for v in volunteers:
             if solver.Value(schedule[(v, d, 2)]) == 1:
                 observer = True
                 break
         if observer:
             line += vol_r[v]
         else:
             line += write_r(' ' * 11, 11)

         # Plus
         for v in volunteers:
             if solver.Value(schedule[(v, d, 3)]) == 1:
                 plus = True
                 break
         if plus:
             line += vol_r[v]
         print(line)
    print()


    # print(str(schedule_year) + ' ' + month_name)
    print()
    for v in volunteers:
         has = False
         for d in list_of_days:
             for s in shifts:
                 if solver.Value(schedule[(v, d, s)]) == 1:
                     if s == 0:
                         t = l_phone
                     elif s == 1:
                         t = l_chat
                     elif s == 2:
                         t = l_observer
                     elif s == 3:
                         t = l_extra
                     if has:
                         print(' ' * 11 + '  {:>2}. {}'.format(d,t))
                     else:
                         print(vol_r[v] + ': {:>2}. {}'.format(d,t))
                     has = True
         if has:
             print()
    print()


    # Who works less than willing?
    print(l_workloads + ': ')
    nonzero_capacity = False
    for v in volunteers:
         works = 0
         more = 0
         workload = all_workload[v]
         for d in list_of_days:
             for s in shifts:
                 if solver.Value(schedule[(v, d, s)]) == 1:
                     works += 1
         more = workload - works
         if more > 0 or more < 0:
             name = volunteer_dic[v]
             nonzero_capacity = True
             print('    {:>10} '.format(name), end='')
             if l_works_a:
                 print(l_works_a + ' ', end='')
             print(str(works), l_day_maybe_plural(works), end='')
             if l_works_b:
                 print(' ' + l_works_b, end='')
             print(', ', end='')
             if l_but_offered_a:
                 print(l_but_offered_a + ' ', end='')
             print(workload, l_day_maybe_plural(workload), end='')
             if l_but_offered_b:
                 print(' ' + l_but_offered_b, end='')
             print('.')
    if not nonzero_capacity:
         print(l_capacity + '.')
    print()

    if l_message_1:
         print()
         print()
         print(l_message_1)
         print(l_message_2)
         print()
         print()
