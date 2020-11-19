#!/usr/bin/python3.7
# @Time : 2020/8/21 0021 10:55 
def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag

    dagParams = DefaultDagParams()
    # 取第一个值
    result = dag(dagParams, pinyinList, path_num=10, log=True)[0].path[0]
    print(result)
    return result


if __name__ == '__main__':
    lists = ['shen', 'zhen']
    pinyin_2_hanzi(lists)
