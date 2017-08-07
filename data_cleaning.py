import re
import pandas as pd
import jieba

import logging

from gensim.models import Word2Vec

data1 = pd.read_csv('U2.csv',encoding='gbk')
data2 = pd.read_csv('U1_tag.csv',encoding = 'gbk')
data3 = pd.read_csv('U2_tag.csv',encoding = 'gbk')
data4 = pd.read_csv('U3_tag.csv',encoding = 'gbk')
data = pd.concat([data1,data2,data3,data4])
comment = data[['position','rateContent']]


stopwords = []
stay_words = []
final_comment = []

seg_list = []

word_freq = {}
freq_word = []


def remove_punc(line):
    punctuation = '/<>b!,;:?"\'！，。？；：“”()（）.\n&#~ '
    l = re.sub(r'[{}]+'.format(punctuation), '', line)
    return l


def remove_num(line):
    t = re.sub(r'/d+','',line)
    return t

# cut sentences and save it as words
def cut(line):
    if type(line) is not float:
        seg_list = jieba.cut(line, cut_all=False)
        line = list(seg_list)
    return line

# delete stopwords and replace synonym:
# texts is the file recording stopwords and synonym dictionary
# seg_list is the list that need to clean
def delete_replace(texts, seg_list):
    texts = ['商品评论停词.txt','替换物流.txt','替换质量.txt',
             '替换性价比.txt','替换态度.txt','替换外观.txt']
    l =[]
    file = open(texts[0],encoding='gbk')
    for line in file:
        line = re.sub(r'\n', '', line)
        l.append(line)
    stopwords = {}.fromkeys(l)

    file = open(texts[1],encoding='gbk')
    s_wuliu = []
    for line in file:
        line = re.sub(r'\n', '', line)
        s_wuliu.append(line)
    print(s_wuliu)
    wuliuwords = {}.fromkeys(s_wuliu)

    file = open(texts[2], encoding='gbk')
    s_zhl = []
    for line in file:
        line = re.sub(r'\n', '', line)
        s_zhl.append(line)
    zhlwords = {}.fromkeys(s_zhl)

    file = open(texts[3], encoding='gbk')
    s_xjb = []
    for line in file:
        line = re.sub(r'\n', '', line)
        s_wuliu.append(line)
    xjbwords = {}.fromkeys(s_xjb)

    file = open(texts[4], encoding='gbk')
    s_taidu = []
    for line in file:
        line = re.sub(r'\n', '', line)
        s_taidu.append(line)
    taiduwords = {}.fromkeys(s_taidu)

    file = open(texts[5], encoding='gbk')
    s_wg = []
    for line in file:
        line = re.sub(r'\n', '', line)
        s_wg.append(line)
    wgwords = {}.fromkeys(s_wg)


    for sentence in seg_list:
        list = []
        for word in sentence:
            if word not in stopwords:
                if word in wuliuwords:
                    word = '物流'
                elif word in zhlwords:
                    word = '质量'
                elif word in  xjbwords:
                    word = '性价比'
                elif word in taiduwords:
                    word = '态度'
                elif word in wgwords:
                    word = '外观'

                stay_words.append(word)
                list.append(word)
                final_comment.extend(list)
        sentence = list
        print(sentence)

    return stay_words,final_comment


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

comment = comment.dropna()
comment['rateContent'] = comment['rateContent'].map(remove_punc,remove_num)
comment = comment.drop_duplicates()

comment = comment.dropna()

comment_c = comment['rateContent'].map(cut)
delete_replace('商品评论停词.txt',comment_c)


def save_freq():
    sort(0)
    save('U盘.txt')


def cleaned_to_csv():
    position = comment['position']
    df = pd.DataFrame({'position':position,
                   'comment':comment_c,})
    df.to_csv('cleaned_USB_1.csv',encoding='utf-8')


#word2vec
def w2v():
    global comment_c
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    num_features = 300
    min_word_count = 1
    num_workers = 1
    context = 5
    downsampling = 1e-3

    print('Training Model ...')
    # train model
    model = Word2Vec(comment_c, workers=num_workers, size=num_features,
                     min_count=min_word_count, window=context, sample=downsampling)


    y2= model.most_similar(u"性价比",topn=30)# 30个最相关的  
    for item in y2:
        similar = open('性价比.txt', 'a')
        similar.write(item[0]+'\n')
        similar.close()


def main():
    global comment
    comment = comment.dropna()
    comment['rateContent'] = comment['rateContent'].map(remove_punc,remove_num)
    comment = comment.drop_duplicates()

    comment = comment.dropna()

    comment_c = comment['rateContent'].map(cut)
    delete_replace('商品评论停词.txt',comment_c)


    sort(0)
    save('U盘.txt')

    position = comment['position']
    df = pd.DataFrame({'position':position,
                   'comment':comment_c,})
    df.to_csv('cleaned_USB_1.csv',encoding='utf-8')

if __name__ == '__main__':
    main()
