import gensim
from gensim.models import Word2Vec
import numpy as np

# Tokenleştirme ve Word2Vec modelini eğiten fonksiyon
def tokenize_and_train_word2vec(corpus):

    # Cümleleri kelimelere ayırarak tokenleştiriyorum
    tokenized_corpus = [sentence.split() for sentence in corpus]
    
    # Word2Vec modelini eğitiyorum
    model = Word2Vec(tokenized_corpus, vector_size=100, window=5, min_count=1, workers=4)
    return model

# Bir cümle için ortalama Word2Vec vektörünü alan fonksiyon
def get_average_word2vec(sentence, model):
   
    # Cümleyi kelimelere ayırma
    tokens = sentence.split()
    
    # Kelimelerin Word2Vec vektörlerini alma
    word_vectors = [model.wv[token] for token in tokens if token in model.wv]
    
    if len(word_vectors) == 0:
        # Eğer cümlede hiç kelime bulunmazsa sıfır vektör döndür
        return np.zeros(model.vector_size)
    
    # Kelimelerin vektörlerinin ortalamasını döndür
    return np.mean(word_vectors, axis=0)
