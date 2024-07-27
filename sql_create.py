import sqlite3
import json

# Kết nối tới database (tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('data.db')

# Tạo một cursor object để tương tác với database
cursor = conn.cursor()

# Tạo bảng
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    history_chat TEXT
)
''')

# Lưu thay đổi
cursor.execute('''
CREATE TABLE IF NOT EXISTS rating (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL,
    point INTEGER NOT NULL,
    username TEXT NOT NULL
)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        username TEXT,
        cong_viec TEXT,
        thoi_gian TEXT,
        dia_diem TEXT,
        luu_y TEXT
    )
''')
conn.commit()

# Tạo dữ liệu mẫu
user1_history = [
    {'role': 'user', 'content': 'hi', 'content_type': 'text'},
    {'role': 'assistant', 'type': 'answer', 'content': 'Chào bạn! Hôm nay bạn thế nào? Có điều gì muốn chia sẻ hay cần mình giúp đỡ không?', 'content_type': 'text'}
]
# Chèn dữ liệu vào bảng, chuyển đổi mảng thành chuỗi JSON
cursor.execute("INSERT INTO users (username, password, history_chat) VALUES (?, ?, ?)", 
               ('TranDuck', '******', json.dumps(user1_history)))
conn.commit()

# Truy vấn dữ liệu
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# In kết quả và chuyển đổi lịch sử trò chuyện từ JSON về mảng Python
for row in rows:
    id, username, password, history_chat = row
    history_chat_list = json.loads(history_chat)
    print(f'ID: {id}, Username: {username}, Password: {password}, History: {history_chat_list}')


# Đóng kết nối
conn.close()
