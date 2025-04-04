from difflib import SequenceMatcher
from functools import lru_cache

import gensim.downloader as api
import nltk
import numpy as np
import spacy
import tensorflow_hub as hub
from fastDamerauLevenshtein import damerauLevenshtein
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import (SparseTermSimilarityMatrix,
                                 WordEmbeddingSimilarityIndex)
from jiwer import wer
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from nltk.translate.nist_score import sentence_nist
from pyter import ter
from rouge import Rouge
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import \
    cosine_similarity as gensim_cosine_similarity


class Metrics:
    def __init__(self, download_models=True):
        if download_models:
            nltk.download('wordnet', quiet = True)
            self.word2vec = self._download_word2vec()
            self.sbert = self._download_sbert()
            self.use_model = self._download_use()
        else:
            self.word2vec = ""
            self.sbert = ""
            self.use_model = ""

        
    @lru_cache(None)
    def _download_word2vec(self):
        #1.6 GB
        return api.load('word2vec-google-news-300')
    @lru_cache(None)
    def _download_sbert(self):
        return SentenceTransformer('paraphrase-MiniLM-L6-v2')
    @lru_cache(None)
    def _download_use(self):
        #for some reason stops working due to caching. 
        #if it errors run rm -rf /var/folders/k2/1_w7z8xn0fb3dh35c1nd4k5c0000gn/T/tfhub_modules/
        return hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    @lru_cache(None)
    def _load_spacy_model(self):
        #run python -m spacy download en_core_web_md
        return spacy.load("en_core_web_md")
    
    # ---------------------------------------------------------------- Lexical ----------------------------------------------------------------
    def exact_match(self, s1: str, s2: str) -> int:
        return 1 if s1 == s2 else 0

    def levenshtein_distance(self, word1: str,  word2: str) -> int:
        #from leetcode
        word1Length = len(word1)
        word2Length = len(word2)
        if word1Length == 0:
            return word2Length
        if word2Length == 0:
            return word1Length
        dp = [
            [0 for _ in range(word2Length + 1)] for _ in range(word1Length + 1)
        ]
        for word1Index in range(1, word1Length + 1):
            dp[word1Index][0] = word1Index
        for word2Index in range(1, word2Length + 1):
            dp[0][word2Index] = word2Index
        for word1Index in range(1, word1Length + 1):
            for word2Index in range(1, word2Length + 1):
                if word2[word2Index - 1] == word1[word1Index - 1]:
                    dp[word1Index][word2Index] = dp[word1Index - 1][
                        word2Index - 1
                    ]
                else:
                    dp[word1Index][word2Index] = (
                        min(
                            dp[word1Index - 1][word2Index],
                            dp[word1Index][word2Index - 1],
                            dp[word1Index - 1][word2Index - 1],
                        )
                        + 1
                    )
        return dp[word1Length][word2Length]
        @lru_cache(None)
        def dp(i, j):
            if i == 0: return j
            if j == 0: return i
            if s1[i-1] == s2[j-1]: return dp(i-1, j-1)
            return min(dp(i-1, j), dp(i, j-1), dp(i-1, j-1)) + 1
        
        return dp(len(s1), len(s2))

            

    def damerau_levenshtein(self, s1: str,  s2: str, similarity: bool = True, deleteWeight: int = 1, insertWeight: int = 1, replaceWeight: int = 1, swapWeight: int = 1) -> int:
        return damerauLevenshtein(s1, s2, similarity, deleteWeight, insertWeight, replaceWeight, swapWeight)

    #higher is worse.
    #might be a good idea to substract from 1
    def WER(self, s1, s2):
        return 1 - wer(s1, s2)

    def levenshtein_distance_words(self, list1: list, list2: list) -> int:
        @lru_cache(None)
        def dp(i, j):
            if i == 0: return j
            if j == 0: return i
            if list1[i - 1] == list2[j - 1]:
                return dp(i - 1, j - 1)
            return min(dp(i - 1, j), dp(i, j - 1), dp(i - 1, j - 1)) + 1
        
        return dp(len(list1), len(list2))
    #pure python wer
    def word_error_rate(self, s1, s2):

        word_distance = self.levenshtein_distance_words(s1, s2)
        return 1 - (word_distance / max(len(s1), 1))

    def TER(self, s1, s2):
        return ter(s1, s2)

    def gestalt_pattern_matching(self, s1, s2):
        matcher = SequenceMatcher(None, s1, s2)
        return matcher.ratio()

    # ---------------------------------------------------------------- Sets ----------------------------------------------------------------

    def jaccard(self, s1, s2):
        s1_set = set(s1)
        s2_set = set(s2)
        return len(s1_set.intersection(s2_set)) / len(s1_set.union(s2_set))

    def overlap_coeff(self, s1, s2):
        s1_set = set(s1)
        s2_set = set(s2)
        return len(s1_set.intersection(s2_set)) / min(len(s1_set), len(s2_set))

    #should probably use sklearns
    def dice_sorensen_coefficient(self, s1, s2):
        s1_set = set(s1)
        s2_set = set(s2)
        return (2 * len(s1_set.intersection(s2_set))) / (len(s1_set) + len(s2_set))

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

    def compute_meteor(self, reference: list, hypothesis: list) -> float:
        #I THINK THIS IS INCORRECT
        #THIS CAN BE CALCULATED WITH ONE CALCULATION IT SEEMS 
        return meteor_score([[reference]], [hypothesis])

    def compute_rouge(self, reference: str, hypothesis: str) -> float:
        #THIS RETURNS A DICTIONARY. NOT SURE HOW I WANT TO COMPARE YET
        return 0
        rouge = Rouge()
        scores = rouge.get_scores(hypothesis, reference) 
        return scores[0]["rouge-1"] # Returns the first score for ROUGE-1, ROUGE-2, and ROUGE-L

    def compute_nist(self, reference: str, hypothesis: str) -> float:
        return 0
        if reference == hypothesis:
            #to avoid a ZeroDivision Error
            return float("inf")
        #print("this is reference " + reference)
        #print("this is hypothesis_text " + hypothesis)
        temp = sentence_nist([reference.split(" ")], hypothesis.split(" "))
        #print("adjflkajdsflkajdsfl;")
        return temp

    def lepor(self, reference: str, hypothesis: str) -> float:
        ...
        #the python package is outdated. Or at least, you need an older version of numpy

    # ---------------------------------------------------------------- Semantic Similarity ----------------------------------------------------------------

    #cosine similarity of word vectors. Words are embedded using the spacy models (above).
    def semantic_similarity_spacy(self, s1: str, s2: str):
        model = self._load_spacy_model()
        s1 = model(s1)
        s2 = model(s2)
        return s1.similarity(s2)

    def _preprocess(self, sentence):
        return [w for w in sentence.lower().split()]

    #embeds the vectors using google's word2vec model. #Smaller is better in this case, so should probably return 1 - wmd
    def wmd(self, s1: str, s2: str):
        if not self.word2vec:
            print ("This metric requires the models to be downloaded")
            return -1
        l1 = self._preprocess(s1)
        l2 = self._preprocess(s2)
        return self.word2vec.wmdistance(l1, l2)

    #cosine similarity, but this time with embedded by word2vec model.  -- This implementation just straight up might be wrong. The scores are too high
    def gensim_cosine(self, s1: str, s2: str):
        if not self.word2vec:
            print ("This metric requires the models to be downloaded")
            return -1
        vec_1 = sum(self.word2vec[word] for word in s1 if word in self.word2vec) / len(s1)
        vec_2 = sum(self.word2vec[word] for word in s2 if word in self.word2vec) / len(s2)
        return gensim_cosine_similarity([vec_1], [vec_2])[0][0]

    def sbert_cosine(self, s1: str, s2: str):
        if not self.sbert:
            print ("This metric requires the models to be downloaded")
            return -1
        vec_1 = self.sbert.encode(s1, convert_to_tensor=True)
        vec_2 = self.sbert.encode(s2, convert_to_tensor=True)
        return util.cos_sim(vec_1, vec_2)[0][0].item()

    #this one uses innerproduct between vectors embedded by the USE model. Can also use cosine, euclidean, and manhattan
    def USE_similarity(self, s1, s2):
        if not self.use_model:
            print ("This metric requires the models to be downloaded")
            return -1
        vec_1 = self.use_model([s1])
        vec_2 = self.use_model([s2])
        return np.inner(vec_1, vec_2)[0][0]

    # also uses word2vec, word frequency (bag of words), Wikipedia: A soft cosine or ("soft" similarity) between two vectors considers similarities between 
    # pairs of features. The traditional cosine similarity considers the vector space model (VSM) features as independent or completely different, while 
    # the soft cosine measure proposes considering the similarity of features in VSM, which help generalize the concept of cosine (and soft cosine) as well 
    # as the idea of (soft) similarity.

    #This implementation gives suspicious results
    def soft_cosine(self, s1: str, s2: str):
        s1 = self._preprocess(s1)
        s2 = self._preprocess(s2)

        documents = [s1, s2]
        dictionary = Dictionary(documents)

        s1 = dictionary.doc2bow(s1)
        s2 = dictionary.doc2bow(s2)

        documents = [s1, s2]
        tfidf = TfidfModel(documents)
        sentence_1 = tfidf[s1]
        sentence_2 = tfidf[s2]
        termsim_index = WordEmbeddingSimilarityIndex(self.word2vec)
        termsim_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary, tfidf)
        return termsim_matrix.inner_product(sentence_1, sentence_2, normalized=(True, True))
        


