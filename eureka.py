# -*- coding:utf-8 -*-


import os
import codecs
import pickle
from tqdm import tqdm
from model import *
import ipdb


def load_dict(f_path):
    # load word dictionary file in format .pkl or .txt
    d = dict()
    if isinstance(f_path, str) and os.path.exists(f_path):
        if f_path.endswith(".pkl"):
            with open(f_path, "rb") as f:
                d = pickle.load(f)
        elif f_path.endswith(".txt"):
            with codecs.open(f_path, 'r', "utf-8") as f:
                lst = f.readlines()
                for w in lst:
                    w = w.strip("\n\t\r").strip()
                    if w in d.keys():
                        pass
                    else:
                        d[w] = True
        else:
            pass
    return d


def filter_word(s):
    # define condition to filter new detected word
    if len(s) < 2:
        return False
    return True


def lst_in_dict(lst, d):
    # input: lst = [w_1, w_2, ...], where w_i = [string, string(float), string(float), ...]
    #      d = {w_1: lst_w_1, w_2: lst_w_2, ...}, where w_j: [string(float), string(float)]
    # output: new d, same format with d, containing updating keys and values
    for w in lst:
        word = w[0]
        if not filter_word(word):
            continue
        lst_v_new = w[1:]
        if word in d.keys():
            lst_v = d.get(word)
            for i_v, v in enumerate(lst_v_new):
                lst_v[i_v] = 0.5 * (lst_v[i_v] + float(v))
            d[word] = lst_v
        else:
            d[word] = [float(v) for v in lst_v_new]
    return d
    

class Eureka(object):

    def __init__(self):
        self.stop_path = "stop_words.txt"
        self.stop_words = dict()
        self.filter_exist = "pkuseg"
        self.r_eval = 0.5
        self.max_word_len = 4

    def load_dictionary(self):
        self.stop_words = load_dict(self.stop_path)

    def discover_corpus(self, corpus):
        # input: corpus is a long string
        # output: lst = [w, w, ...], where w = (word, length, freq, pmi, entropy)
        lst = list()
        if isinstance(corpus, str) and 0 < len(corpus) < 300000:
            lst = discover_words(corpus, 
                          stop_words=self.stop_words,
                          filter_exist=self.filter_exist,
                          r_eval=self.r_eval,
                          max_word_len=self.max_word_len)
        return lst

    def save_corpus(self, lst, save_path="result_now.csv"):
        # input: lst = [w, w, ...], where w = (word, length, freq, pmi, entropy)
        #        save_path is a string endswith .csv or .pkl
        # output: True for successfully saving or False
        tag = False
        if not isinstance(lst, list) or len(lst) == 0 or not isinstance(save_path, str):
            return tag
        if save_path.endswith(".csv"):
            tag = save_csv(lst, save_path=save_path)
        elif save_path.endswith(".pkl"):
            tag = save_pkl(lst, save_path=save_path)
        else:
            pass
        return tag
    
    def discover_corpus_multi(self, corpus_all, corpus_size=200000, re_list=True):
        # input: corpus_all is a very long string, e.g., a book or many concatenated documents
        #     corpus_size is int, the number of words for each corpus
        #     re_list = True to return lst, False to return dict
        # output: lst = [w, w, ...], where w = (word, length, freq, pmi, entropy) / dict = {word: [word, length, freq, pmi, entropy]}
        if not isinstance(corpus_all, str) or len(corpus_all) == 0:
            res = list() if re_list else dict()
            return res
        
        print("Detect candidates ...")
        res = dict()  # res = {word: [word, length, freq, pmi, entropy]}
        corpus = ""
        corpus_count = 0
        for i_i, i in enumerate(corpus_all):
            if corpus_count > corpus_size:
                print(i_i)
                lst_r = self.discover_corpus(corpus)
                res = lst_in_dict(lst_r, res)
                corpus = i
                corpus_count = 1
            else:
                corpus += i
                corpus_count += 1
        
        if re_list:
            print("Dictionary to lists ...")
            lst = list()
            for k, v in res.items():
                w = [k] + v
                lst.append(w)
            res = rank_words(lst, r_eval=self.r_eval)
        return res
    
    def discover_corpus_mongo(self, col=None, n=20000, corpus_size=200000, re_list=True):
        # input: col is a mongodb collections, each sample in col must has the key "content" to store the text
        #     n is int, number of news used in new word detection
        #     corpus_size is int, the number of words for each corpus
        #     re_list = True to return lst, False to return dict
        # output: lst = [w, w, ...], where w = (word, length, freq, pmi, entropy) / dict_ = {word: [word, length, freq, pmi, entropy]}
        if col is None or col.count() == 0 :
            res = list() if re_list else dict()
            return res
        
        print("Detect candidates ...")
        res = dict()  # res = {word: [word, length, freq, pmi, entropy]}
        corpus = ""
        corpus_count = 0
        for i in tqdm(col.find().limit(n)):
            text = i.get("content")
            if corpus_count > corpus_size:
                lst_r = self.discover_corpus(corpus)
                res = lst_in_dict(lst_r, res)
                corpus = text
                corpus_count = len(text)
            else:
                corpus += text
                corpus_count += len(text)
        
        if re_list:
            print("Dictionary to lists ...")
            lst = list()
            for k, v in res.items():
                w = [k] + v
                lst.append(w)
            res = rank_words(lst, r_eval=self.r_eval)
        return res


if __name__ == "__main__":
    corpus = codecs.open("document.txt", "r", "utf-8").read()
    eureka = Eureka()
    eureka.load_dictionary()
    lst = eureka.discover_corpus(corpus)
    tag = eureka.save_corpus(lst, "result_now.pkl")
    print(tag)
