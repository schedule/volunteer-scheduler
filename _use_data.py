def use_data(id, type, days_available, workload,
     max_weekend_days, welcomes_observer, separate_w, alone,
     cannot_alone, not_with):

     all_days_available.append(days_available)
     all_workload.append(workload)

     # Volunteers doing only chat
     if type == l_C:
         for d in list_of_days:
             for s in [0,2]:
                 model.Add(schedule[(id, d, s)] == False)
             if d in days_available:
                 model.Add(sum(schedule[(id, d, s)]
                         for s in [1,3]) <= 1)
             else:
                 for s in [1,3]:
                     model.Add(schedule[(id, d, s)] == False)

     # Volunteers doing chat and phone
     if type == l_CP:
         for d in list_of_days:
             model.Add(schedule[(id, d, 2)] == False)
             if d in days_available:
                 model.Add(sum(schedule[(id, d, s)]
                         for s in [0,1,3]) <= 1)
             else:
                 for s in [0,1,3]:
                     model.Add(schedule[(id, d, s)] == False)

     # Volunteers doing only phone
     if type == l_P:
         for d in list_of_days:
             for s in [1,2]:
                 model.Add(schedule[(id, d, s)] == False)
             if d in days_available:
                 model.Add(sum(schedule[(id, d, s)]
                         for s in [0,3]) <= 1)
             else:
                 for s in [0,3]:
                     model.Add(schedule[(id, d, s)] == False)

     # Volunteers doing observation
     if type == l_O:
         observers.append(id)
         for d in list_of_days:
             for s in [0,1,3]:
                 model.Add(schedule[(id, d, s)] == False)
             if d in days_available:
                 model.Add(schedule[(id, d, 2)] <= 1)
             else:
                 model.Add(schedule[(id, d, 2)] == False)

     # List observers and volunteers welcoming observers
     if type in [l_C, l_CP, l_P] and welcomes_observer:
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
         for i in weeks:
             model.Add(sum(schedule[(id, d, s)]
                 for s in shifts for d in weeks[i]
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
