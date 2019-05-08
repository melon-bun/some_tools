# -*- coding: utf-8 -*-
"""
"""

import pandas as pd
import itertools

def swapCol(df, cols:list, value_col):
    dict_ = {}
    ix = 0
    
    for i in range(df.shape[0]):
        pair = tuple([df.loc[i,col_name] for col_name in cols])
        value = df.loc[i,value_col]
        #如果这个标签对存在，则累加相应的数值
        if pair in dict_:
            dict_[pair][1]+=value
        #如果这个标签对不存在字典内，则生成这个标签对的所有组合可能，加入字典
        else:
            all_pairs = list(itertools.permutations(pair, len(pair)))
            for i in all_pairs:
                dict_[i] = [ix,0]
            ix+=1
            dict_[pair][1]+=value
    
    temp_df = pd.DataFrame(dict_).T
    temp_df.rename(columns = {0:'ix',1:'value'},inplace=True)
    pairs_ix = temp_df.drop_duplicates('ix').reset_index().drop('value',axis=1)
    combine_ix = temp_df.groupby(['ix'])['value'].sum().reset_index()
    res = pairs_ix.merge(combine_ix,left_on='ix',right_on='ix')
    return res
    pass

# For example
if __name__=="__main__":
    df = pd.DataFrame([['上海','北京',12],['北京','上海',11],
                       ['北京','上海',5],['绍兴','上海',3],
                       ['c','a',77],['b','c',12]],columns=['Source','Target','Value'])
    df1 = pd.DataFrame([['上海','北京','杭州',12],['北京','杭州','上海',11],
                       ['北京','上海','宁波',5],['绍兴','上海','北京',3],
                       ['c','a','b',77],['b','c','a',12]],columns=['Source','Target','Mid','Value'])
    res1 = swapCol(df,['Source','Target'],'Value')
    res2 = swapCol(df1,['Source','Target','Mid'],'Value')
    print(res1)
    print(res2)
#dff.drop_duplicates(0)
