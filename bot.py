from flask import Flask
import rocket-bot

app = Flask(__name__)

@app.route("/")
def hello():
    rocket-bot.init()
    return "Bot started."