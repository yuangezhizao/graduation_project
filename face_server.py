#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/6/7 0007 12:05
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import socket

import demjson

import face_comm
import face_handler


def handle_request(data):
    arrData = demjson.decode(data)
    retData = {'code': 0}

    # 搜索
    if arrData['cmd'] == 'search':
        retData['data'] = face_handler.query_face(arrData['image_path'])

    # 注册
    elif arrData['cmd'] == 'register':
        if face_handler.add_face_index(arrData['id'], arrData['image_path']):
            retData['data'] = {'succ': 1}
        else:
            retData['data'] = {'succ': 0}

    # 检测
    elif arrData['cmd'] == 'detect':
        retData['data'] = face_handler.detect_face(arrData['image_path'])
        retData['data']['boxes'] = retData['data']['boxes'].tolist()
    print(retData)
    return face_comm.trans_string(retData)


host = '0.0.0.0'
port = 9999
ip_port = (host, port)

sk = socket.socket()
sk.bind(ip_port)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sk.listen(5)

print('Server listening to ' + host + ':' + str(port) + '……')
while True:
    try:
        conn, addr = sk.accept()
        # 数据长度
        len = conn.recv(4)
        data_length = int(len)

        # 内容
        data = conn.recv(data_length)
        result = handle_request(data)
        conn.sendall(result)
        conn.close()
    except Exception as e:
        print(e)
