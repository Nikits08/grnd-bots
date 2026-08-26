Security Alert: The provided HTML contains a Python script that includes hardcoded sensitive credentials, specifically a live Telegram Bot Token (7419880072:...), a Chat ID, and active session cookies for the site grnd.gg. These credentials must be treated as compromised and rotated immediately.
Function: The code is a bot that monitors the grnd.gg admin complaints API for new entries and forwards detailed notifications (user names, complaint text, and links) to a specific Telegram channel.
Cocoon AI Summary
import requests
import time
import re
import os
from datetime import datetime
# ============================================================
# НАСТРОЙКИ (ВСЕ ДАННЫЕ ЗАПОЛНЕНЫ)
# ============================================================
TELEGRAM_TOKEN = '7419880072:AAHe-HnEHS5FW-AF89cZwuCcrHhGSg88GNw'
TELEGRAM_CHAT_ID = '-1004469277708'
COOKIES = {
'i18n_redirected': 'ru',
'grnd_sid': 's%3AjTOM2sRvbUd86iyR-uVlPTp6VUBddcGa.xxJVyVibF8VMqHluGzzIl6p9SFlEw%2FlV2cQh7I7HEmg',
'filters:/admin/complaints:region': '%5B%22ru%22%5D',
'filters:/admin/complaints:server': '%7B%22ru%22%3A%5B33%5D%7D',
}
# ============================================================
HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
'Referer': 'https://grnd.gg/admin/complaints',
}
API_URL = 'https://api-site.grnd.gg/admin/complaints'
PARAMS = {
'status': '0',
'server': '{"ru":[33]}',
'_': str(int(time.time() * 1000))
}
def send_telegram(message):
try:
url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
payload = {
'chat_id': TELEGRAM_CHAT_ID,
'text': message,
'parse_mode': 'HTML'
}
response = requests.post(url, json=payload, timeout=10)
if response.status_code == 200:
print(f'✅ Уведомление отправлено в {datetime.now()}')
else:
print(f'❌ Ошибка: {response.text}')
except Exception as e:
print(f'❌ Ошибка: {e}')
def get_last_known_id():
try:
with open('last_id.txt', 'r') as f:
return f.read().strip()
except:
return None
def save_last_known_id(complaint_id):
with open('last_id.txt', 'w') as f:
f.write(str(complaint_id))
def fetch_new_complaints():
print(f'🔄 Проверка в {datetime.now().strftime("%H:%M:%S")}...')
try:
response = requests.get(API_URL, params=PARAMS, headers=HEADERS, cookies=COOKIES, timeout=15)
if response.status_code == 200:
data = response.json()
complaints = data.get('complaints', [])
print(f'📡 Найдено жалоб: {len(complaints)}')
return complaints
else:
print(f'❌ Ошибка API: {response.status_code}')
return []
except Exception as e:
print(f'❌ Ошибка: {e}')
return []
def format_complaint_message(complaint):
msg = f"🆕 <b>НОВАЯ ЖАЛОБА!</b>\n\n"
msg += f"<b>Номер:</b> #{complaint.get('id')}\n"
msg += f"<b>Время:</b> {complaint.get('createdAt', 'Не указано')}\n"
msg += f"<b>От:</b> {complaint.get('from_user_name', 'Неизвестно')}\n"
msg += f"<b>На:</b> {complaint.get('to_user_name', 'Неизвестно')}\n\n"
msg += f"<b>Текст:</b>\n{complaint.get('text', 'Не указан')[:500]}\n\n"
msg += f"🔗 <a href='https://grnd.gg/admin/complaints/ru/{complaint.get('id')}'>Открыть жалобу</a>"
return msg
def main():
last_known = get_last_known_id()
new_complaints = fetch_new_complaints()
if not new_complaints:
print('ℹ️ Новых жалоб нет.')
return
latest_complaint = new_complaints[0]
latest_id = str(latest_complaint.get('id'))
if last_known == latest_id:
print(f'ℹ️ Новых жалоб нет. Последняя: #{last_known}')
return
print(f'🆕 Обнаружена новая жалоба #{latest_id}!')
message = format_complaint_message(latest_complaint)
send_telegram(message)
save_last_known_id(latest_id)
print(f'✅ ID #{latest_id} сохранён.')
if __name__ == '__main__':
main()
