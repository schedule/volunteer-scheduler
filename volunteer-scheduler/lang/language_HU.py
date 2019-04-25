l_filename = 'data/data_HU.csv'
l_output_filename = 'beosztas'
l_encoding = 'UTF8'
l_after_year = '.'
l_month_name_dic = {1:'január', 2:'február', 3:'március', 4:'április',
        5:'május', 6:'június', 7:'július', 8:'augusztus', 9:'szeptember',
        10:'október', 11:'november', 12:'december'}
l_weekday_name_list = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek',
        'Szombat', 'Vasárnap']
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
l_need = 'Szükség van még az alábbiakra:'
l_created = 'Új fájl:'
l_message_1 = '"Köszönöm, hogy rendelkezésre álltok a hozzátok fordulóknak."'
l_message_2 = '- A beosztást elkészítő szoftver írója'
