import requests
import json
import os
import uuid
#------------------------------------------------------------------------------
uuid_organization = ''
uuid_conversation = ''
cookie = ''
link = 'https://claude.ai/api/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0'
header_b = {"User-Agent": f"{user_agent}","Referer": "https://claude.ai/chat","Origin": "https://claude.ai","Content-Type": "application/json","Accept-Language": "en-US,en;q=0.5" }
#------------------------------------------------------------------------------
class Anthropic():
      #------------------------------------------------------------------------------
      def load_cookie():
          global cookie
          with open(f'{os.getcwd()}/claude.json', "r", encoding="utf-8") as file:
              data = json.load(file)
              if isinstance(data, list):
                  for item in data:
                      if item.get("name") == "sessionKey":
                          cookie = item.get("value")
      #------------------------------------------------------------------------------
      def generate_uuid():
          random_uuid = uuid.uuid4()
          random_uuid_str = str(random_uuid)
          formatted_uuid = f"{random_uuid_str[0:8]}-{random_uuid_str[9:13]}-{random_uuid_str[14:18]}-{random_uuid_str[19:23]}-{random_uuid_str[24:]}"
          return formatted_uuid
      #------------------------------------------------------------------------------
      def create_new_chat():
          global link, uuid_organization, uuid_conversation,  cookie, user_agent, header_b
          payload = json.dumps({"uuid": Anthropic.generate_uuid(), "name": ""})
          headers = {"Accept": "*/*","Connection": "keep-alive","Cookie": f"sessionKey={cookie}",}
          headers.update(header_b)
          requests.request("POST", f"{link}organizations/{uuid_organization}/chat_conversations", headers=headers, data=payload)
      #------------------------------------------------------------------------------
      def get_organization_id():
          global link, uuid_organization, uuid_conversation,  cookie, user_agent, header_b
          headers = {"Cookie": f"sessionKey={cookie}",}
          headers.update(header_b)
          response = requests.get(f"{link}organizations", headers=headers)
          data = response.json()
          uuid_organization = data[0]['uuid']
      #------------------------------------------------------------------------------
      def list_conversation():
          global link, uuid_organization, uuid_conversation,  cookie, user_agent, header_b
          headers = {"Cookie": f"sessionKey={cookie}",}
          headers.update(header_b)
          try:
              response = requests.get(f"{link}organizations/{uuid_organization}/chat_conversations", headers=headers)
              data = response.json()
              uuid_conversation = data[0]['uuid']
          except Exception as e:
              Anthropic.create_new_chat()
              Anthropic.list_conversation()
      #------------------------------------------------------------------------------
      def send_message_direct(prompt):
          Anthropic.load_cookie()
          texto = Anthropic.send_message(prompt)
          Anthropic.delete_conversation()
          return texto
      #------------------------------------------------------------------------------        
      def send_message(prompt):
          global link, uuid_organization, uuid_conversation,  cookie, user_agent, header_b
          if uuid_organization == '' or uuid_conversation == '':
              Anthropic.get_organization_id()
              Anthropic.list_conversation()

          payload = json.dumps({
            "completion": {
              "prompt": f"{prompt}",
              "timezone": "America/Sao_Paulo",
              "model": "claude-2"
            },
            "organization_uuid": f"{uuid_organization}",
            "conversation_uuid": f"{uuid_conversation}",
            "text": f"{prompt}",
            "attachments": []
          })
          headers = {"Accept": "text/event-stream, text/event-stream","Cookie": f"sessionKey={cookie}",}
          headers.update(header_b)
          try:
              response = requests.post(f"{link}append_message", headers=headers, data=payload, stream=True)
              data = response.text.strip().split('\n')[-1]
              data = data.encode('latin1').decode('utf-8')
              answer = json.loads(data[6:])['completion']
              return {"answer": json.loads(data[6:])['completion']}['answer']
          except Exception as e:
              pass
      #------------------------------------------------------------------------------
      def delete_conversation():
          global link, uuid_organization, uuid_conversation,  cookie, user_agent, header_b
          payload = json.dumps(f"{uuid_conversation}")
          headers = {'Accept': '*/*',"Cookie": f"sessionKey={cookie}",'Content-Length': '38'}
          headers.update(header_b)
          requests.request("DELETE", f"{link}organizations/{uuid_organization}/chat_conversations/{uuid_conversation}", headers=headers, data=payload)
#------------------------------------------------------------------------------
print(Anthropic.send_message_direct("quero suco de uva como fazer ?"))
