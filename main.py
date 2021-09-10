# coding: utf-8

import MeCab
import collections 
import numpy as np
from pymagnitude import Magnitude
from statistics import mode
import csv
import pprint

def get_concept_number(quest:str) -> list:
    """
    正規化処理のために概念と数量のlistを取得する。

    Parameters
    ----------
    quest : str
        問題文
    
    Returns
    -------
    concept_number_tuple : list
        序数詞に1番近い一般名詞tuple型にしてlistに格納
    """


    m = MeCab.Tagger("-Ochasen")
    node = m.parseToNode(quest)
    words=[]
    nums=[]
    verbs = []
    concept_number_tuple = []

    i = 1

    while node:
        hinshi = node.feature.split(",")[1]
        if hinshi in ["一般"]:
            # print(node.surface)
            origin = node.feature.split(",")[6]
            words.append((origin,i))

        if hinshi in ["数"]:
            # print(node.surface.split(","))
            origin = node.surface.split(",")[0]
            nums.append((origin,i))
        

        if node.feature.split(",")[0] in ["動詞","助動詞"] :
            # print(node.surface.split(","))
            origin = node.surface.split(",")[0]
            verbs.append((origin,i))
        node = node.next
        
        i += 1

    for num in nums:
        min_string = words[0][0]
        min_diff = 9999
        for word in words:
            diff = abs(word[1] - num[1])
            if diff < min_diff:
                min_string = word[0]
                min_diff = diff
            
            min_verbs = verbs[0][0]
            min_vdiff = 99998
            for verb in verbs:
                vdiff = abs(word[1] - verb[1])
                if vdiff < min_vdiff:
                    min_verbs = verb[0]
                    min_vdiff = vdiff
        # print("({},{})".format(min_string,num[0]))
        # min_stringとnumのtuple型をlistに格納
        # concept_number_tuple.append((min_string,num[0]))
        
        concept_number_tuple.append((min_string,num[0],min_verbs))


    return concept_number_tuple
        
    
def get_standard_list(normalize_list:list) -> list:
    """
    概念と数量のlistから共通概念処理されたlistを作成

    Parameters
    ----------
    normalize_list : list
        序数詞に1番近い一般名詞tuple型にしてlistに格納
    
    Returns
    -------
    standard_list : list
        共通概念処理されたlist
    """
    vectors = Magnitude("chive-1.2-mc5.magnitude")
    standard_list = []
    normalize_word_set = set([normalizeword_tuple[0] for normalizeword_tuple in normalize_list])
    duplicate_list = []
    allduplicate_list = []

    for word in normalize_list:
        # vectors.most_similar(word[0], topn=10)はtuple型のlistである.
        # 単語のリスト化を行う
        word_set = set([word_tuple[0] for word_tuple in vectors.most_similar(word[0], topn=10) ])
        #重複単語のリスト化
        duplicate_list = list((normalize_word_set & word_set))
        allduplicate_list.extend(duplicate_list)
    #allduplicate_listの再頻出単語
    base_word = (mode(allduplicate_list))
    for normalize_word in normalize_list:
        standard_list.append((base_word,normalize_word[1],normalize_word[2]))
    return standard_list

if __name__ == "__main__":
    with open('/workspace/NLP-Container/data/sample_questions.csv' , encoding ="utf_8") as f:
        reader = csv.reader(f)
        quest_list = [row for row in reader]
    quest = quest_list[2][4]
    normalize_list = get_concept_number(quest)
    print(normalize_list)
    print("正規化処理完了")
    standard_list = get_standard_list(normalize_list)
    print("共通概念処理完了")
    print(standard_list)