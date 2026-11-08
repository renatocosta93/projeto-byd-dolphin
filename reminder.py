import os
import json
import urllib.request

# O comando .strip() remove qualquer espaço invisível copiado sem querer pelo celular
BOT_TOKEN = os.environ['TELEGRAM_TOKEN'].strip()
CHAT_ID = os.environ['TELEGRAM_CHAT_ID'].strip()
PANEL_URL = os.environ['PANEL_URL'].strip()

try:
    with open('last_message_id.txt', 'r') as f:
        last_id = f.read().strip()
    
    if last_id:
        delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={CHAT_ID}&message_id={last_id}"
        urllib.request.urlopen(delete_url)
except Exception as e:
    print(f"Nao deletou anterior: {e}")

msg = "🚗 Boa noite! Você teve novos custos ou fez alguma recarga no Dolphin Mini hoje?\n\nAcesse o painel para manter a sua amortização atualizada."

keyboard = {
    "inline_keyboard": [[{"text": "📊 Abrir Painel BYD", "url": PANEL_URL}]]
}

send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = json.dumps({
    "chat_id": CHAT_ID,
    "text": msg,
    "reply_markup": keyboard
}).encode('utf-8')

req = urllib.request.Request(send_url, data=data, headers={'Content-Type': 'application/json'})
response = urllib.request.urlopen(req)
res_data = json.loads(response.read().decode('utf-8'))

new_id = res_data['result']['message_id']
with open('last_message_id.txt', 'w') as f:
    f.write(str(new_id))
