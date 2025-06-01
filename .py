import json
import random
from datetime import datetime

FRASES = [
    "Acredite em você mesmo e tudo será possível!",
    "Cada passo conta, mesmo os mais lentos.",
    "O sucesso é a soma de pequenos esforços diários.",
    "Você consegue! Nunca subestime sua força interior",
    "Persistência é o caminho do êxito.",
    "Não espere por oportunidades. Crie-as.",
    "Seja a mudança que você deseja ver no mundo.",
]

def obter_nome(event):
    try:
        body_str = event.get("body")
        if not body_str:
            return "Visitante"
        body = json.loads(body_str)
        return body.get("nome", "Visitante")
    except Exception as e:
        print("Erro ao ler nome:", str(e))
        return "Visitante"

def gerar_frase():
    id_frase = random.randint(0, len(FRASES) - 1)
    return id_frase, FRASES[id_frase]

def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event))  

    nome = obter_nome(event)
    id_frase, frase = gerar_frase()

    mensagem = f"{frase}, {nome}"
    response = {
        "mensagem": mensagem,
        "frase_id": id_frase + 1,  
        "gerado_em": datetime.utcnow().isoformat() + "Z"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response),
        "headers": {
            "Content-Type": "application/json"
        }
    }
