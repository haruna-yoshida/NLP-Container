# coding: utf-8

import MeCab
import collections 
import numpy as np

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
    concept_number_tuple = []

    i = 1

    while node:
        hinshi = node.feature.split(",")[1]
        if hinshi in ["一般"]:
            origin = node.feature.split(",")[6]
            words.append((origin,i))

        if hinshi in ["数"]:
            origin = node.surface.split(",")[0]
            nums.append((origin,i))
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
        # print("({},{})".format(min_string,num[0]))
        # min_stringとnumのtuple型をlistに格納
        concept_number_tuple.append((min_string,num[0]))
    
    return concept_number_tuple
        

if __name__ == "__main__":
    quest = str("あめが64個あります。36人の子どもに1個ずつ分けると、あめは何個あまりますか。")
    concept_number_list = get_concept_number(quest)
    print(concept_number_list)