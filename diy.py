# -*- coding: UTF-8 -*-
import gc
import json
import sys
import os

import numpy
from matplotlib import pyplot as plt
sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages/')
sys.path.insert(1, 'C:/Python27/Lib/site-packages')
import networkx as nx
def print_obj(obj):
    "打印对象的所有属性"
    print(obj.__dict__)

import pickle

def get_first_info(element):
    G = element.old_g
    # print_obj(G)
    block_num = len(G._pred)
    in_degrees = []
    for i in range(block_num):
        in_degrees.append([])
    edge_num = 0
    adj_matrix = []
    for i in range(block_num):
        adj_matrix.append([])
        for j in range(block_num):
            if i in G._pred[j]:
                adj_matrix[i].append(j)
                edge_num += 1
    # for i in range(block_num):
    #     print(adj_matrix[i])
    # print(edge_num)
    # print(in_degrees)
    return [block_num, edge_num, adj_matrix]

def get_original_filename(filename):    # 去后缀
    p = filename.split('\\')
    return p[-1]

def get_info(f):
    gc.collect()
    testpath = f
    print testpath
    fr = open(testpath, 'r')
    data1 = pickle.load(fr)

    for element in data1.raw_graph_list:
        current_list = {}  # 一个函数的特征字典
        current_list['src'] = get_original_filename(f)  # 文件名
        features = []
        current_list['fname'] = element.funcname  # 函数名
        print element.funcname
        G = element.g
        current_list['n_num'] = len(G)  # 节点数量

        for i in range(len(G)):
            temp = G.node[i]['v']
            t = len(temp[0])
            temp[0] = len(temp[1])
            temp[1] = t
            del temp[6]
            for i in range(7):
                temp[i] = round(float(temp[i]), 1)
            features.append(temp)
        current_list['features'] = features
        current_list['succs'] = get_first_info(element)[2]
        whole_list.append(current_list)
    return whole_list

def write_file(out, list):
    print out
    if not os.path.isfile(out):
        with open(out, 'w+') as json_file:
            all_info = []
            for i in list:
                if i not in all_info:
                    all_info.append(i)
            json.dump(all_info, json_file)
    else:
        all_info = []
        with open(out, 'r') as json_file:
            all_info = json.load(json_file)
        with open(out, 'w') as json_file:
            for i in list:
                if i not in all_info:
                    all_info.append(i)
            json.dump(all_info, json_file)

#sub_10F20 308  反编译代码有字符串，但是这个特征提取里没有字符串 constant，可能是间接引用的，不识别。看了下所有函数的特征，几乎都没有字符串常量，可能都是写在别的地方然后引用的。
#sub_166C4 393
if __name__ == '__main__':

    whole_list = []
    target_filename = sys.argv[2]

    file = sys.argv[1]
    if os.path.isfile(file):
        info = get_info(file)
        for i in info:
            whole_list.append(i)
    elif os.path.isdir(file):
        for root, dir, files in os.walk(file):
            for f in files:
                if f.split('.')[-1] == 'ida':   # 这是一个ida文件
                    info = get_info(root + "\\\\" + f)
                    for i in range(len(info)):
                        whole_list.append(info[i])
                    if len(whole_list) > 30:
                        write_file(target_filename, whole_list)
                        del whole_list
                        whole_list = []

    write_file(target_filename, whole_list)
    del whole_list
    # no_repeated_list = []
    #
    # for w in whole_list:
    #     if w not in no_repeated_list:
    #         no_repeated_list.append(w)
    #
    # s = json.dumps(no_repeated_list)
    # print s
    # print len(whole_list)
    # print(whole_list)
    # print len(no_repeated_list)
    #
    # with open('.\\cfg.json', 'w') as f:
    #     f.write(s)

    exit(0)

    testpath = '.\\ida_files\\b_print_0.ida'
    fr = open(testpath, 'r')
    data1 = pickle.load(fr) #一个二进制文件的acfgs
    #print(type(data1))
    #print_obj(data1)
    #print data1.raw_graph_list[393]
    #print_obj(data1.raw_graph_list[393])
    #nx.draw(data1.raw_graph_list[393].g,with_labels=True)
    #plt.show()

    print "一个二进制文件的所有函数的原始特征，list。"
    print_obj(data1) #acfg list
    print "\n"

    print "一个函数的原始特征，由old_g（discovRe方法的ACFG），g（Genius方法的ACFG），fun_feature（表示函数级别的特征的向量）三部分构成"
    for element in data1.raw_graph_list:
        print('\nfunction name: ' + element.funcname + "\n")
        # print_obj(element)
        # print_obj(data1.raw_graph_list[393]) #一个函数的acfg
        # feature=data1.raw_graph_list[393].fun_features
        # feature = element.fun_features
        # print feature

        G = element.g
        for i in range(len(G)):
            print(G.node[i]['v'])

        func_info = get_first_info(element)
        # print_obj(element.old_g)
    # print "函数级别特征： # 1 function calls # 2 logic instructions # 3 TransferIns # 4 LocalVariables # 5 BB basicblocks# 6 Edges # 7 IncommingCalls# 8 Intrs# 9 between # 10 strings # 11 consts"

        print "\n"


    # G=data1.raw_graph_list[393].old_g
    # print G.node[0] # G.node[i]是dict
    # for key, value in G.node[0].items():
    #     print('{key}:{value}'.format(key=key, value=value))

    # 一个基本块的特征 #1'consts' 数字常量 #2'strings'字符串常量 #3'offs' offspring 字节点数量？ #4'numAs' 算数指令如INC  #5'numCalls' 调用指令 #6'numIns' 指令数量 #7'numLIs' LogicInstructions 如AND #8'numTIs' 转移指令数量
    # G=data1.raw_graph_list[0].g
    # print "# 一个基本块的特征 #1'consts' 数字常量 #2'strings'字符串常量 #3'offs' offspring 字节点数量？ #4'numAs' 算数指令如INC  #5'numCalls' 调用指令 #6'numIns' 指令数量 #7'numLIs' LogicInstructions 如AND #8'numTIs' 转移指令数量"
    # print G.node[0]
    # print "\n"
    # for key, value in G.node[0].items():
    #     print('{key}:{value}'.format(key=key, value=value))



    #oldg就是读取IDA的CFG，所以数量、方向等都一样；g根据old_g生成，也一样
    #old g

    # G = data1.raw_graph_list[0].old_g
    # print_obj(G)
    # block_num = len(G._pred)
    # in_degrees = []
    # for i in range(block_num):
    #     in_degrees.append(0)
    # edge_num = 0
    # adj_matrix = []
    # for i in range(block_num):
    #     adj_matrix.append([])
    #     for j in range(block_num):
    #         if i in G._pred[j]:
    #             adj_matrix[i].append(1)
    #             in_degrees[j] += 1
    #             edge_num += 1
    #         else:
    #             adj_matrix[i].append(0)
    # for i in range(block_num):
    #     print(adj_matrix[i])
    # print(edge_num)
    # print(in_degrees)

    # nx.draw(G,with_labels=True)
    # plt.title('old_g')
    # plt.show()


    # g
    # G = data1.raw_graph_list[0].g
    # nx.draw(G,with_labels=True)
    # #plt.title('Genius_g')
    # plt.show()

    # # draw graph with labels
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos)
    # node_labels = nx.get_node_attributes(G, 'v')  #networkx的node，由属性。g的属性为'v'，意为原始特征的vector。old_g的属性见cfg_constructor.py
    # nx.draw_networkx_labels(G, pos, labels=node_labels)
    # #plt.title('Genius_g with raw feature vector')
    # plt.show()