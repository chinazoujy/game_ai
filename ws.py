# -*- coding: utf-8 -*-
import websocket
import thread
import time
import json
import sm

__author__ = 'zoujinyong'


# 接受服务器发送的信息
def on_message(ws, message):
    mess = json.loads(message)
    if mess['type'] == "picking":
        print message
        print "Picking Hero...."
        # shooter or warrior
        pick_hero = '{"type": "pickHero", "heros": ["warrior", "warrior", "warrior", "warrior", "warrior"]}'
        ws.send(pick_hero)
    elif mess['type'] == "update":
        cmds = sm.update(mess)
        if cmds is None or len(cmds) == 0:
            return

        for command in cmds:
            ws.send(command)
        #print message
    elif mess['type'] == "cmdError":
        print message

def on_error(ws, error):
    on_open(ws)
    print "Error:", error

def on_close(ws):
    on_open(ws)
    print "### closed ###"

def on_open(ws):
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print "thread terminating..."
    # thread.start_new_thread(run, ())
    #join_room = '{"type": "join","gameId": "15v15","token": "XIzOiZmNmiZiqsAa", "isRed":true}'

    join_room = '{"type": "join","gameId": "15v00","token": "XIzOiZmNmiZiqsAa"}'
    ws.send(join_room)
    #ws.send(join_room_2)


if __name__ == "__main__":
    websocket.enableTrace(True)
    url = ""
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
