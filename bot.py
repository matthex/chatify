from flask import Flask
import rocket_bot

app = Flask(__name__)

@app.route("/")
def hello():
    rocket_bot.init()
    return "Bot started."