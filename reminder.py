import os
import json
import urllib.request
from urllib.error import HTTPError

BOT_TOKEN = os.environ['TELEGRAM_TOKEN'].strip()
CHAT_ID = str(os.environ['TELEGRAM_CHAT_ID']).strip()
PANEL_URL = os.environ['PANEL_URL'].strip()

# Conserta automaticamente o link se faltar o https://
if not PANEL_URL.startswith("http"):
    PANEL_URL = "https://" + PANEL_URL

try:
    with open('last_message_id.txt', 'r') as f:
        last_id = f.read().strip()
    if last_id:
        delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage?chat_id={CHAT_ID}&message_id={last_id}"
        urllib.request.urlopen(delete_url)
except Exception:
    pass

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

try:
    response = urllib.request.urlopen(req)
    res_data = json.loads(response.read().decode('utf-8'))
    new_id = res_data['result']['message_id']
    with open('last_message_id.txt', 'w') as f:
        f.write(str(new_id))
except HTTPError as e:
    erro_telegram = e.read().decode('utf-8')
    print("\n" + "="*50)
    print(f"ERRO EXATO DO TELEGRAM: {erro_telegram}")
    print("="*50 + "\n")
    raise
