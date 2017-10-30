import json
from watson_developer_cloud import ConversationV1
from os import environ

class watson_conversation:

    name='bluemix'

    def __init__(self):
        #get config from heroku config vars
        config = json.loads(environ[name])

        username = config["bluemix-service-user"]
        password = config["bluemix-service-password"]
        global workspace_id
        workspace_id = config["bluemix-service-workspace"]

        global conversation
        conversation = ConversationV1(
            username = username,
            password = password,
            version = '2017-04-21',
            url = "https://gateway-fra.watsonplatform.net/conversation/api")

    def analyze(self, message):
        response = conversation.message(workspace_id = workspace_id, message_input = {
            'text': message})
        print(json.dumps(response, indent=2))
        if len(response['intents']) > 0:
            return response['intents'][0]['intent']
        else:
            return "-99"