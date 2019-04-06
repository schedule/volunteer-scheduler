from _use_data import *

def add_data():
    all_days_available = []
    all_workload = []
    all_cannot_alone = []
    all_not_with = []

    # List of volunteers welcoming observers and list of observers:
    welcomers = []
    observers = []

    # List of volunteers who cannot work alone
    cannot_work_alone = []

    # List of volunteer who does not want to work with some others
    not_with_them = []


    # Processing file data

    # volunteer_dic = {ID:name}, volunteer_dic_r = {name:ID}
    volunteer_dic = {}
    volunteer_dic_r = {}
    id = 0
    for line in data_lines:
         volunteer_dic[id] = f[line][1]
         volunteer_dic_r[f[line][1]] = id
         id += 1

    def bool_from_string(value):
         bool(int(value))

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

         use_data(id, type, days_available, workload,
             max_weekend_days, welcomes_observer, separate_w, alone,
             cannot_alone, not_with)
         id += 1
