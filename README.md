# Projeto AWS Lambda: Frases Motivacionais Personalizadas

Este projeto implementa uma função Lambda simples em Python que retorna uma **frase motivacional aleatória**, personalizada com o nome fornecido pelo usuário.

---

## Sumário

- [Objetivo da Função](#objetivo-da-função)
- [Formato da Entrada](#formato-da-entrada)
- [Formato da Saída](#formato-da-saída)
- [Linguagem e Ambiente](#linguagem-e-ambiente)
- [Como Testar](#como-testar)
- [Logs e Depuração](#logs-e-depuração)
- [Código-Fonte](#código-fonte)
- [Requisitos e Observações](#requisitos-e-observações)

---

## Objetivo da Função

A função tem como finalidade gerar uma frase motivacional aleatória e personalizá-la com um nome recebido no corpo da requisição. Caso o nome não seja informado, o valor padrão é **"Visitante"**.

---

## Formato da Entrada

A função espera receber uma requisição com o campo `body` contendo um JSON stringificado com o campo `nome`.

### Exemplo de entrada válida via API Gateway ou Postman:

```json
{
  "body": "{\"nome\": \"Carlos\"}"
}
```

Se o campo `body` estiver ausente ou não contiver um JSON válido com `nome`, a função utilizará "Visitante".

---

## Formato da Saída

A resposta é um JSON com código HTTP 200 e um corpo que inclui:

* `mensagem`: Frase motivacional personalizada.
* `frase_id`: Índice (1 baseado) da frase sorteada.
* `gerado_em`: Data/hora UTC da geração da frase.

### Exemplo de resposta:

```json
{
  "statusCode": 200,
  "body": "{\"mensagem\": \"Persistência é o caminho do êxito., Carlos\", \"frase_id\": 5, \"gerado_em\": \"2025-06-01T12:00:00.000000Z\"}",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

---

## Linguagem e Ambiente

* **Linguagem:** Python
* **Runtime AWS Lambda:** `python3.9` (ou superior)
* **Serviços utilizados:**
  - AWS Lambda
  - CloudWatch Logs (para depuração)

---

## Como Testar

### Console AWS Lambda

1. Acesse a função Lambda no Console da AWS.
2. Crie um evento de teste com o seguinte conteúdo:

```json
{
  "body": "{\"nome\": \"Maria\"}"
}
```

Ou, sem nome:

```json
{
  "body": "{}"
}
```

3. Clique em "Test" para verificar a execução e visualizar a resposta gerada.

---

### Postman

1. **Método:** `POST`  
2. **URL:** URL da Function (exposta via Function URL da AWS)
3. **Headers:**

```
Content-Type: application/json
```

4. **Body (raw - JSON):**

```json
{
  "nome": "Carlos"
}
```

---

## Logs e Depuração

A função utiliza `print()` para registrar eventos recebidos e erros, facilitando a depuração via **AWS CloudWatch Logs**.

### Como acessar os logs:

1. No Console da AWS, acesse o serviço **CloudWatch**.
2. Vá em **Logs** > **Log groups**.
3. Busque pelo grupo:  
   ```
   /aws/lambda/NOME_DA_FUNÇÃO
   ```
4. Clique sobre o grupo e escolha a execução mais recente (log stream).
5. Os logs exibem informações como:
   - Evento recebido
   - Problemas ao obter o nome do JSON

#### Exemplo de saída no log:

```
Evento recebido: {"body": "{\"nome\": \"Carlos\"}"}
```

> 💡 **Dica:** Você pode adicionar mais `print()` no código para depurar outras partes do fluxo, como o nome recebido ou erros específicos.

---

## Código-Fonte

```python
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
```

---
