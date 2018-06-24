print ("Api ai OBZ Module Loaded")
from app.mac import mac, signals
import apiai,uuid
import simplejson as json
from pymongo import MongoClient

#connect
client = MongoClient('mongodb://localhost:27017/')
#db
db = client['bot']
userdata = db['userdata']

ai = apiai.ApiAI('56b329557b3148d99e1b4f9ce286efa4')

#globals
nome = ""
presente = False
respondeu = False
motivo = ""
opiniao = ""
feedback = ""

@signals.message_received.connect
def handle(message):
    global nome
    global presente
    global respondeu
    global motivo
    global opiniao
    global feedback
    if not message.text == "":
        nome = message.who_name
        request = ai.text_request()
        request.lang = 'pt-br'
        request.query = message.text
        print ("Mensagem de %s: %s"%(nome,message.text))
        response = request.getresponse()
        response_data = json.loads(response.read())
        result = response_data['result']
        parameters = result['parameters']
        fulfillment = result['fulfillment']
        speech = fulfillment['speech']
        print("Resposta: "+speech)
        mac.send_message(speech, message.conversation)
        action = result['action']
        print ("Action: "+action)
        print ("Nome: " +nome)


        presente = False
        respondeu = False
        motivo = ""
        opiniao = ""
        feedback = ""
        #Pega nome
        if action == 'start':
            if not parameters['nome'] == "":
                nome = parameters['nome']


        #Estaria presente
        if action == 'presente.sim':
           presente = True
           userdata.update({'nome':nome},{'$set':{'presente':presente}},upsert=True)

        #Não estaria presente    
        elif action == 'presente.nao':
            presente = False
            userdata.update({'nome':nome},{'$set':{'presente':presente}},upsert=True)
        #Poderia responder
        if action == 'poderiaresponder.sim':
            respondeu = True
            userdata.update({'nome':nome},{'$set':{'respondeu':respondeu}},upsert=True)
        #Não poderia responder
        elif action == 'poderiaresponder.nao':
            respondeu = False
            userdata.update({'nome':nome},{'$set':{'respondeu':respondeu}},upsert=True)
        #Feedback (Não poderia responder)
        if action == 'feedback':
            if not parameters['feedback'] == "":
                feedback = parameters['feedback']
                userdata.update({'nome':nome},{'$set':{'feedback':feedback}},upsert=True)
            else:
                feedback = "Sem feedback"
                userdata.update({'nome':nome},{'$set':{'feedback':feedback}},upsert=True)
        #Motivo
        if action == 'motivo':
            if not parameters['number'] == "":
                motivo = parameters['number']
                userdata.update({'nome':nome},{'$set':{'motivo':motivo[0]}},upsert=True)
            else:
                motivo = "Sem motivo"
                userdata.update({'nome':nome},{'$set':{'motivo':motivo[0]}},upsert=True)

        #Opiniao
        if action == 'opiniao':
            if not parameters['number'] == "":
                opiniao = parameters['number']
                userdata.update({'nome':nome},{'$set':{'opiniao':opiniao[0]}},upsert=True)
            else:
                opiniao = "Sem opiniao"
                userdata.update({'nome':nome},{'$set':{'opiniao':opiniao[0]}},upsert=True)