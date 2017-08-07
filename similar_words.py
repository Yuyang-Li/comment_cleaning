import pandas as pd
import logging
import os.path


from gensim.models import Word2Vec

content = pd.read_csv('cleaned_USB_1_1.csv')['comment']



def w2v():
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    num_features = 300
    min_word_count = 1
    num_workers = 1
    context = 5
    downsampling = 1e-3
    model_name = '{}features_{}minwords_{}context.model'.format(
        num_features, min_word_count, context)
    print('Training Model ...')
    # train model
    model = Word2Vec(content, workers=num_workers, size=num_features,
                     min_count=min_word_count, window=context, sample=downsampling)


    y2= model.most_similar(u"快",topn=30)# 20个最相关的  
    for item in y2:
        similar = open('快递.txt', 'a')
        similar.write(item[0]+'\n')
        similar.close()

w2v()



def to_review_vector(review):
    words = w2s(review)
    array = np.array([model[w] for w in words if w in model])
    return pd.Series(array.mean(axis=0))

