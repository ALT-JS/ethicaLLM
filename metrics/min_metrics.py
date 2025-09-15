from functools import lru_cache

import nltk
import numpy as np
import tensorflow_hub as hub
from fastDamerauLevenshtein import damerauLevenshtein

from nltk.translate.bleu_score import sentence_bleu
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Metrics:
    def __init__(self, download_models=True):
        if download_models:
            nltk.download('wordnet', quiet = True)
            self.use_model = self._download_use()
        else:
            self.use_model = ""

        
    @lru_cache(None)
    def _download_use(self):
        #for some reason stops working due to caching. 
        #if it errors run rm -rf /var/folders/k2/1_w7z8xn0fb3dh35c1nd4k5c0000gn/T/tfhub_modules/
        return hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    
            
    def damerau_levenshtein(self, s1: str,  s2: str, similarity: bool = True, deleteWeight: int = 1, insertWeight: int = 1, replaceWeight: int = 1, swapWeight: int = 1) -> int:
        return damerauLevenshtein(s1, s2, similarity, deleteWeight, insertWeight, replaceWeight, swapWeight)


    # ---------------------------------------------------------------- Cosine Similarity ----------------------------------------------------------------
    def compute_cosine_similarity(self, s1: str, s2: str, method: str = 'tf-idf') -> float:    
        if method == 'word_frequency':
            vectorizer = CountVectorizer()  #word frequency embedding
        elif method == 'tf-idf':
            vectorizer = TfidfVectorizer()  #tf-idf embedding
        else:
            raise ValueError("Some other embeddings")

        vectors = vectorizer.fit_transform([s1, s2])
        vectors_array = vectors.toarray()
        
        similarity = cosine_similarity(vectors_array[0:1], vectors_array[1:2])
        
        return similarity[0][0]

    # ---------------------------------------------------------------- BLEU related ----------------------------------------------------------------
    def compute_bleu(self, reference: list, hypothesis: list) -> float:
        return sentence_bleu([reference], hypothesis)

    def USE_similarity(self, s1, s2):
        if not self.use_model:
            print ("This metric requires the models to be downloaded")
            return -1
        vec_1 = self.use_model([s1])
        vec_2 = self.use_model([s2])
        return np.inner(vec_1, vec_2)[0][0]
