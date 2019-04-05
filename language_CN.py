filename = 'data_CN.csv'
after_year = '年'
month_name_dic = {1:'一月', 2:'二月', 3:'三月', 4:'四月',
    5:'五月', 6:'六月', 7:'七月', 8:'八月', 9:'九月',
    10:'十月', 11:'十一月', 12:'十二月'}
l_C = 'C'
l_CP = 'CP'
l_P = 'P'
l_O = 'O'
l_Day = '日'.encode('gb18030').rjust(9).decode('gb18030')
l_Phone = '电话'.encode('gb18030').rjust(11).decode('gb18030')
l_Chat = '网聊'.encode('gb18030').rjust(10).decode('gb18030')
l_Observer = '观察'.encode('gb18030').rjust(10).decode('gb18030')
l_phone = '电话'
l_chat = '网聊'
l_observer = '观察'
l_workloads = '工作量'
l_capacity = '所有志愿者的工作量达到原来提供的日数'
l_works_a = '被安排'
l_works_b = ''
def l_day_maybe_plural(day):
    if day > 1:
        return '天'
    else:
        return '天'
l_but_offered_a = '但想工作'
l_but_offered_b = ''
