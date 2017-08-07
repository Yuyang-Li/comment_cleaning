# -*- coding: utf-8 -*-    # import system default encoding
import re


# no missing data
def missing_data(comment):
    comment['content'].fillna(0)
    comment = comment[comment != 0]

# remove punctuation
def remove_punc(line):
    punctuation = '!,;:?"\'！，。？；：“”().'
    l = re.sub(r'[{}]+'.format(punctuation), '', line)
    return l

def remove_num(line):
    t = re.sub(r'/d','',line)
    return t

def main():
    # format unified
    comment['content'] = comment['content'].map(remove_punc,remove_num)

    # remove duplicate value
    comment = comment['content'].drop_duplicates()
    comment = comment.dropna()

    # save
    comment.to_csv('test1.csv',encoding='utf-8')


if __name__ =='__main__':
    main()
