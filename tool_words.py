# -*- coding: utf-8 -*-
import pandas as pd
import re
import jieba

df = pd.read_csv('comment.csv')
content = df['好']

com = []

stopwords = []
stay_words = []
final_comment = []

word_freq = {}
freq_word = []


# cut sentences and save it as words
def cut(line):
    if type(line) is not float:
        seg_list = jieba.cut(line, cut_all=False)
        line = list(seg_list)
        com.append(line)

    return com

# delete stopwords:
# text is the file recording stopwords
# seg_list is the list that need to clean
def delete(text,seg_list):
    l =[]
    file = open(text)
    for line in file:
        line = re.sub(r'\n', '', line)
        l.append(line)
    stopwords = {}.fromkeys(l)

    for sentence in seg_list:
        list = []
        for word in sentence:
            if word not in stopwords:
                stay_words.append(word)
                list.append(word)
        final_comment.append(list)

    return stay_words,final_comment


# word frequency
def sort(max_number):
    for word in stay_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    for word, freq in word_freq.items():
        freq_word.append((word, freq))
    freq_word.sort(key=lambda x: x[1], reverse=True)

    for word, freq in freq_word[: max_number]:
        print(word, freq)
    return freq_word


# save the sort result into f_sort
def save(f_sort):
    file = open(f_sort,'w',encoding='utf-8')
    for word,freq in freq_word:
        file.write(word+str(freq)+'\n')
    file.close()


# improve stopwords list
def add_words(append_list,text):
    file = open(text,'a+')
    for word in file:
        file.write(word + '\n')
    file.close()


# run
def main():
    content.map(cut)
    delete('neg.0.txt',com)
    sort(0)
    save('路由器分词.txt')


if __name__ == '__main__':
    main()