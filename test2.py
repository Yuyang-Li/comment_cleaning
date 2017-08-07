import pandas as pd

pd = pd.read_csv('U1_tag.csv',encoding='gbk')
comment = pd[['position','rateContent']]
print (comment)


for item in y2:
    similar = open('快递.txt', 'a')
    similar.write(str(item[0]) + '\n')
    similar.close()

def save():
    seg_list = []
    seg_list = seg_list.map(for_series)
    return stay_words,final_comment,seg_list