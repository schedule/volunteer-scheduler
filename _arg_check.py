import sys

def arg_check():
   try:
       language = sys.argv[1]
       if language == 'EN':
           from language_EN import *
       elif language == 'HU':
           from language_HU import *
       elif language == 'CN':
           from language_CN import *
       else:
           print()
           print('Error: Wrong language code.')
           print('Choose between EN/HU/CN.')
           print()
           sys.exit()
   except IndexError:
       print()
       print('Error: Missing language code.')
       print()
       print('Usage:')
       print('1. Choose language: EN/HU/CN.')
       print('2. Export corresponding data_XX.csv file into a spreadsheet, '
               'fill in your data, then export back into this file.')
       print('3. Run command: python3 schedule.py XX')
       print()
       sys.exit()
