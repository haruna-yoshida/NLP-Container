# coding: utf-8

import MeCab
import collections 
import numpy as np
from pymagnitude import Magnitude
from statistics import mode
import csv
import pprint

def get_node_info(quest:str) -> (list,list):
    """
    mecabを用いて引数用のnodeを生成する

    Parameters
    ----------
    quest : str
        問題文
    
    Returns
    -------
    node_features : list
    node_surfaces : list
        node（形態素解析されたもの）を返す
    """

    m = MeCab.Tagger("-Ochasen")
    node = m.parseToNode(quest)
    node_features = []
    node_surfaces = []
    while node:
        node_features.append(node.feature)
        node_surfaces.append(node.surface)
        node=node.next
    return node_features[1:-1], node_surfaces[1:-1]


def get_concept_number(quest:str,node_features:list,node_surfaces:list):
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
    
    words=[]
    nums=[]
    verbs = []
    concept_number_tuple = []
    
    i = 1

    for node_feature, node_surface in zip(node_features,node_surfaces):
        hinshi = node_feature.split(",")[1]
        if hinshi in ["一般"]:
            # print(node_surface)
            origin = node_feature.split(",")[6]
            words.append((origin,i))
            

        if hinshi in ["数"]:
            # print(node_surface.split(","))
            origin = node_surface.split(",")[0]
            nums.append((origin,i))
        

        if node_feature.split(",")[0] in ["動詞","助動詞"] :
            # print(node_surface.split(","))
            origin = node_surface.split(",")[0]
            verbs.append((origin,i))
        
        
        
        i += 1


    for num in nums:
        min_string = words[0][0]
        min_index = words[0][1]
        min_diff = 9999
        for word in words:
            diff = abs(word[1] - num[1])
            if diff < min_diff:
                min_string = word[0]
                min_index = word[1]
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
        
        concept_number_tuple.append((min_string,num[0],min_verbs,min_index))


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
        standard_list.append((base_word,normalize_word[1],normalize_word[2],normalize_word[3]))
    return standard_list

def get_normalize_table(quest:str,node_features:list,node_surfaces:list):
    #変化明示語からbefore,increaseなどに分ける
    m = MeCab.Tagger("-Ochasen")
    node = m.parseToNode(quest)
    important_words = []
    keywords = []
    concept_number_tuple = []
    table = []

    i = 1
    
    for node_feature, node_surface in zip(node_features,node_surfaces):
        keywords = node_surface.split(",")
        for time_expression_word in time_expression_words:
            for keyword in keywords:
                #print(keyword)
                # print(time_expression_word[0])
                if time_expression_word[0] == keyword:
                    important_words.append((keyword,i,time_expression_word[1]))
        i += 1
                
    # print(important_words)
            # print(node_surface)
            # origin = node_feature.split(",")[6]
            # keywords.append((keyword,i))
            # print(keywords)
                
    for important_word in important_words:
        min_element = standard_list[0]
        # print(standard_list)
        min_diff = 9999
        for element in standard_list:
            diff = abs(element[3] - important_word[1])
            print("{0}:{2} - {1}{3}  = {4}".format(element[0],important_word[0],element[3],important_word[1],diff))
            if diff < min_diff:
                min_element = element
                min_diff = diff
        table.append({important_word[2]:min_element}) 
        print(table)
            
        
        
        


if __name__ == "__main__":
    with open('/workspace/NLP-Container/data/sample_questions.csv' , encoding ="utf_8") as f:
        reader = csv.reader(f)
        quest_list = [row for row in reader]
    quest = quest_list[14][4]
    print(quest)
    with open('/workspace/NLP-Container/data/time_expression_base.csv', encoding ="utf_8") as f:
        reader = csv.reader(f)
        time_expression_word_list = [row for row in reader]
    time_expression_words = time_expression_word_list[1:]
    # print(time_expression_words)
    node_features,node_surfaces = get_node_info(quest)
    normalize_list = get_concept_number(quest,node_features,node_surfaces)
    print("正規化処理完了")
    print(normalize_list)
    standard_list = get_standard_list(normalize_list)
    print("共通概念処理完了")
    print(standard_list)
    normalize_table = get_normalize_table(quest,node_features,node_surfaces)
    print(get_normalize_table)
    
