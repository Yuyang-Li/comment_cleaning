import pandas as pd
import os

file_path = 'C:/Users\Lily\Documents\Lily\DAILY\CPP\观点口碑分析\中文情感挖掘酒店评论语料\ChnSentiCorp_htl_unba_10000/neg'
list = os.listdir(file_path)

joint_list = []
error_list = []

os.chdir(file_path)
for file in list:
    try:
        t = open(file,encoding='gbk').read()
        joint_list.append(t)
    except UnicodeDecodeError:
        error_list.append(file)

df = pd.DataFrame({'sort':'0',
              'content':joint_list})
os.chdir('C:/Users\Lily\Documents\Lily\DAILY\CPP\观点口碑分析')

df1 = pd.read_csv('pos_1.csv')
df2 = pd.read_csv('pos_2.csv')
df3 = pd.read_csv('pos_3.csv')
df4 = pd.read_csv('pos_4.csv')
df_pos = pd.concat([df1,df2,df3,df4])
df_pos.to_csv('pos.csv',columns = ['content','sort'],index = False)

