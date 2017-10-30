import websocket
from rocketchat_API.rocketchat import RocketChat
import time
import json
from watson_container import watson_conversation
from os import environ
import weather
import joke

name='rocketbot'

def init():
    global weburl       #url of chat server
    global socketurl    #socket url of chat server
    global room         #room-id to listen on
    global token        #token for login
    global user_id      #bot's user id
    global rocket       #rocketchat
    global ws           #websocket
    global conversation #bluemix conversation

    #get config from heroku config vars
    config = json.loads(environ[name])

    #constants
    weburl = config["weburl"]
    socketurl = config["socketurl"]
    room = config["room"]
    conversation = watson_conversation()

    #login to get token
    rocket = RocketChat(server_url=weburl)
    login_json = rocket.login(config["user"], config["password"]).json()
    token = login_json.get('data').get('authToken')
    user_id = login_json.get('data').get('userId')
    
    #open websocket
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socketurl,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def on_message(ws, message):
    print(message)
    process_message(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    init()

def on_open(ws):
    print("### open ###")
    connect(ws)
    login(ws)
    subscribe_room(ws)

def connect(ws):    
    ws.send(json.dumps({
        "msg": "connect",
        "version": "1",
        "support":[ "1" ]
    }))

def login(ws):
    ws.send(json.dumps({
        "msg": "method",
        "method": "login",
        "id": "42",
        "params":[
            { "resume": token }
        ]
    }))

def subscribe_room(ws):
    ws.send(json.dumps({
        "msg": "sub",
        "id": "43",
        "name": "stream-room-messages",
        "params":[
            room,
            False
        ]
    }))

def process_message(message):
    msg_json = json.loads(message)
    if is_msg(msg_json) and is_not_by_bot(msg_json):
        msg_text = msg_json['fields']['args'][0]['msg']
        #do something clever with the message
        intent = conversation.analyze(msg_text)
        if intent == 'weather':
            get_weather()
        elif intent == 'joke':
            get_joke()

def is_msg(msg_json):
    #check whether received string is a message
    if 'msg' in msg_json and msg_json['msg'] == "changed" and msg_json['collection'] == "stream-room-messages":
        return True
    else:
        return False

def is_not_by_bot(msg_json):
    #check whether message is from another user than the bot itself
    if msg_json['fields']['args'][0]['u']['_id'] != user_id:
        return True
    else:
        return False

def bot_reply(msg_text):
    rocket.chat_post_message(msg_text, room)

def get_weather():
    bot_reply(weather.get_weather())

def get_joke():
    bot_reply(joke.get_joke())

if __name__ == "__main__":
    init()