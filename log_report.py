import json
import os
import sqlite3
import requests
import re

# Gọi database
db = sqlite3.connect('data.db')
cursor = db.cursor()
# API Của coze
API_URL = "https://api.coze.com/open_api/v2/chat"
psn_token = "pat_NyD4nlGvOto9c7OoSISO6x3uqQhgN0oO3rtNewgdvpXNw9RZk7FHjNFHT2oFa4nR"
header = {
    "Authorization": f'Bearer {psn_token}',
    "Content-type": 'application/json',
    'Connection': "keep-alive",
    "Accept": "*/*",
}
history = []
data2 = {
    "conservation_id": "demo-0",
    "bot_id": "7377038220523700242",
    "user": "demo-user",
    "query": "Hãy xem như tôi là bác sĩ và báo cáo tình hình sức khỏe tin thần của tôi và dự đoán xu hướng sức khỏe tin thần giống như bạn là người thân của tôi đang nói chuyện với bác sĩ, nếu bạn biết tên của tôi thì hãy dùng trong báo cáo",
    "stream": False,
    "chat_history": history,
}
# Menu chọn chức năng
select_mode = input("Nhập: (1: Lịch sử trò chuyện ; 2: Báo cáo tình hình sức khỏe tinh thần): ")
username = input("Nhập username cần truy vấn: ")

if select_mode == "1":
    # Truy vấn lịch sử chat từ database theo username
    cursor.execute("SELECT history_chat FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        history_chat = row[0]
        history = json.loads(history_chat)
    # Tạo file log
    with open(username + '_log' + '.txt', 'w', encoding='utf-8') as file:
        for res in history:
            if 'type' in res:
                message = "GenFriend: "+res['content']
            else:
                message = username+": "+res['content']
            print(message)
            file.write(message + '\n')
            
else:
    # Truy vấn lịch sử chat từ database theo username
    cursor.execute("SELECT history_chat FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        history_chat = row[0]
        history = json.loads(history_chat)
    data2["chat_history"] = history
    data = json.dumps(data2)
    # Request một bảng báo cáo từ GenAI
    res = requests.post(API_URL, data=data, headers=header)
    if res.status_code == 200:
        Ai_ans = [ans['content'] for ans in res.json()['messages'] if ans['type'] == "answer"]
    # Tạo file báo cáo
    output = re.sub(r'\[tên người dùng\]', username, Ai_ans[0],flags=re.IGNORECASE)
    with open(username + '_report' + '.txt', 'w', encoding='utf-8') as file:
        file.write(output+ '\n')