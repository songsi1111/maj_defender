"""
这个程序用于监听互联网中的websocket流量，并通过xmlrpc服务器为其他程序提供数据
"""
# -*- coding: utf-8 -*-
import os
import mitmproxy.http
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import threading
import pickle

import mitmproxy.addonmanager
import mitmproxy.connection
import mitmproxy.http as http
import mitmproxy.log
import mitmproxy.tcp
import mitmproxy.websocket
import mitmproxy.proxy
from xmlrpc.server import SimpleXMLRPCServer
import logging

from liqi import tamperUsetime,LiqiProto

activated_flows = [] # store all flow.id ([-1] is the recently opened)
messages_dict = dict() # flow.id -> List[flow_msg]
liqi = LiqiProto()

with open("save.txt",'w') as f: # 清空文件
    pass
class ClientWebSocket:

    def __init__(self):

        pass

    # Websocket lifecycle

    def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
        """

            Called when a client wants to establish a WebSocket connection. The

            WebSocket-specific headers can be manipulated to alter the

            handshake. The flow object is guaranteed to have a non-None request

            attribute.

        """
        logging.info('[handshake websocket]:',flow,flow.__dict__,dir(flow))

    def websocket_start(self, flow: http.HTTPFlow):
        """

            A websocket connection has commenced.

        """
        logging.info(f'[new websocket]: {flow}')
        global activated_flows,messages_dict
        activated_flows.append(flow.id)
        messages_dict[flow.id]=flow.websocket.messages

    def websocket_message(self, flow: http.HTTPFlow):
        """

            Called when a WebSocket message is received from the client or

            server. The most recent message will be flow.messages[-1]. The

            message is user-modifiable. Currently there are two types of

            messages, corresponding to the BINARY and TEXT frame types.

        """
        assert flow.websocket is not None  # make type checker happy
        message = flow.websocket.messages[-1]
        
        # This is cheating, extending the time limit to 7 seconds
        #tamperUsetime(flow_msg)
        #result = liqi.parse(flow_msg)
        #print(result)
        #print('-'*65)

        if message.from_client:
            logging.info(f"Client sent a message: {message.content!r}")
        else:
            logging.info(f"Server sent a message: {message.content!r}")
            with open("save.txt",'a') as f:
                f.write(f"{message.content}")
                f.write("\n")


addons = [
    ClientWebSocket()
]

# RPC调用函数


def get_len() -> int:
    global activated_flows,messages_dict
    L=messages_dict[activated_flows[-1]]
    return len(L)


def get_item(id: int):
    global activated_flows,messages_dict
    L=messages_dict[activated_flows[-1]]
    return pickle.dumps(L[id])


def get_items(from_: int, to_: int):
    global activated_flows,messages_dict
    L=messages_dict[activated_flows[-1]]
    return pickle.dumps(L[from_:to_:])


def RPC_init():
    server = SimpleXMLRPCServer(('localhost', 37247))
    server.register_function(get_len, "get_len")
    server.register_function(get_item, "get_item")
    server.register_function(get_items, "get_items")
    print("RPC Server Listening on 127.0.0.1:37247 for Client.")
    server.serve_forever()


RPC_server = threading.Thread(target=RPC_init)
RPC_server.start()

# open chrome and liqi
chrome_options = Options()
chrome_options.add_argument('--proxy-server=127.0.0.1:8080')
chrome_options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(options=chrome_options)
# browser.get('https://game.maj-soul.com/1/')

# if __name__=='__main__':
#     #回放websocket流量
#     replay_path=os.path.join(os.path.dirname(__file__), 'websocket_frames.pkl')
#     history_msg = pickle.load(open(replay_path, 'rb'))
#     activated_flows = ['fake_id']
#     messages_dict = {'fake_id':history_msg}