# coding:utf-8
import random

from pymysql import *
import json
import sys
import networkx as nx
from matplotlib import pyplot as plt
import pickle
import hashlib


def connection(database_key):
    mysql = {'host': '', 'port': 3306, 'user': 'root', 'passwd': '', 'db': '', 'charset': 'utf8'}
    if database_key == 'test':
        mysql['host'] = 'localhost'
        mysql['passwd'] = '20030509@Lhy'
        mysql['db'] = 'features'
    return mysql

def create_table(filename):
    conn = connect(**connection("test"))
    conn.cursor().execute("create table `{}`("
                          "`id` int not null auto_increment,"
                          "`name` varchar(100),"
                          "`func_call` int not null,"
                          "`logic_inst` int not null,"
                          "`transin` int not null,"
                          "`localvar` int not null,"
                          "`BBbasic` int not null,"
                          "`edges` int not null,"
                          "`incomming_call` int not null,"
                          "`intrs` int not null,"
                          "`betw` numeric(10, 6) not null,"
                          "`strings` varchar(1024),"
                          "`consts` varchar(8192),"
                          "primary key(`id`)"
                          ")comment'函数特征';".format(filename))

def insert_data(feature_list, filename, funcname=''):
    conn = connect(**connection("test"))
    cursor = conn.cursor()
    command = 'insert into {}(name, func_call, logic_inst, transin, localvar, BBbasic, edges, incomming_call, '\
                   'intrs, betw, strings, consts, version) values(\'{}\', {}, {}, {}, {}, {}, {}, {}, {}, {}, \'{}\', \'{}\', \'{}\');'.format(
                   filename, funcname, feature_list[0], feature_list[1], feature_list[2], feature_list[3], feature_list[4], feature_list[5],
        feature_list[6], feature_list[7], feature_list[8], json.dumps(feature_list[9]), json.dumps(feature_list[10]), '0.9.8a')
    print(command)
    cursor.execute(command)


if __name__ == '__main__':
    testpath = sys.argv[1]
    index = sys.argv[2]
    if index == '':
        table_created = False
        table_name = testpath.split('\\')[-1].split('.')[0]
        create_table(table_name)
        fr = open(testpath, 'r')
        data1 = pickle.load(fr)
        graph_list = data1.raw_graph_list
        for i in range(len(graph_list)):
            print graph_list[i].fun_features
            insert_data(graph_list[i].fun_features, i, table_name)
        print testpath + " created"
    else:
        table_name = 'features'
        try:
            create_table(table_name)
        except Exception:
            pass
        finally:
            fr = open(testpath, 'r')
            data1 = pickle.load(fr)
            graph_list = data1.raw_graph_list
            for i in range(len(graph_list)):
                if graph_list[i].funcname == index:
                    insert_data(graph_list[i].fun_features,
                                'features', graph_list[i].funcname)
