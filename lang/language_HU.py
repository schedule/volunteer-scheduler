filename = 'data/data_HU.csv'
encoding = 'UTF8'
after_year = '.'
month_name_dic = {1:'Január', 2:'Február', 3:'Március', 4:'Április',
    5:'Május', 6:'Június', 7:'Július', 8:'Augusztus', 9:'Szeptember',
    10:'Október', 11:'November', 12:'December'}
l_Name = 'Név'
l_C = 'C'
l_CP = 'CT'
l_P = 'T'
l_O = 'H'
l_E = 'T'
l_Day = 'Nap'
l_Phone = 'Telefon'
l_Chat = 'Cset'
l_Observer = 'Hospitál'
l_Extra = 'Telefon 2'
l_phone = 'telefon'
l_chat = 'cset'
l_observer = 'hospitál'
l_extra = 'telefon'
l_workloads = 'Kapacitások'
l_capacity = 'A munkabeosztás minden kapacitást maradéktalanul felhasznál'
l_works_a = ''
l_works_b = 'dolgzik'
def l_day_maybe_plural(day):
    if day > 1:
        return 'napot'
    else:
        return 'napot'
l_but_offered_a = 'de'
l_but_offered_b = 'ajánlott fel'
l_message_1 = '"Köszönöm, hogy rendelkezésre álltok a hozzátok fordulóknak."'
l_message_2 = ' - A beosztást elkészítő szoftver írója (imreszakal.com)'
