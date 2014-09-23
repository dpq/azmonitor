#!/usr/bin/python
# -*- coding: utf-8 -*-
import websocket
import thread, time, ssl, json
from blessings import Terminal

t = Terminal()

def on_message(ws, message):
    data = sorted(json.loads(message), key=lambda x: x[0])
    row = 0
    with t.location(0, 0):
        print "Unit ID    Lat        Lon       Alt       Temp    Humidity  Pressure"
    for i in range(len(data)):
        if time.time() - data[i][1] > 60:
            color = t.red
        else:
            color = t.normal
        with t.location(0, i+1):
            print color + data[i][0]
        with t.location(10, i+1):
            print round(data[i][2],3)
        with t.location(20, i+1):
            print round(data[i][3],3)
        with t.location(30, i+1):
            print round(data[i][4],2)
        with t.location(40, i+1):
            print round(data[i][3],2)
        with t.location(52, i+1):
            print round(data[i][5],2)
        with t.location(61, i+1):
            print round(data[i][6],2)
    print t.normal

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(1)
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
  try:
    t.enter_fullscreen()
    print t.clear()
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://az.skyhunter.ca:8083/",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
  except:
    print t.normal
    t.exit_fullscreen()
    print t.clear()
    exit()