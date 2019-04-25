l_filename = 'data/data_CN.csv'
l_output_filename = '时间表'
l_encoding = 'gb18030'
l_after_year = '年'
l_month_name_dic = {1:'一月', 2:'二月', 3:'三月', 4:'四月',
        5:'五月', 6:'六月', 7:'七月', 8:'八月', 9:'九月',
        10:'十月', 11:'十一月', 12:'十二月'}
l_weekday_name_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六',
        '星期天']
l_Name = '名字'
l_C = 'C'
l_CP = 'CP'
l_P = 'P'
l_O = 'O'
l_E = 'E'
l_Day = '日'.encode(l_encoding).rjust(9).decode(l_encoding)
l_Phone = '电话'.encode(l_encoding).rjust(11).decode(l_encoding)
l_Chat = '网聊'.encode(l_encoding).rjust(11).decode(l_encoding)
l_Observer = '观察'.encode(l_encoding).rjust(11).decode(l_encoding)
l_Extra = '额外'.encode(l_encoding).rjust(11).decode(l_encoding)
l_phone = '电话'
l_chat = '网聊'
l_observer = '观察'
l_extra = '额外'
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
l_need = '我们还需要人做这些工作：'
l_created = '新文件：'
l_message_1 = ''
l_message_2 = ''
