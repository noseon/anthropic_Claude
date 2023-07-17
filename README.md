from anthropic_Claude.core import Anthropic

Anthropic.load_cookie()
print(Anthropic.send_message("qual seu nome ?"))
Anthropic.delete_conversation()
