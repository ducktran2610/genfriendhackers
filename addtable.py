import sqlite3

# Kết nối đến cơ sở dữ liệu (hoặc tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Tạo bảng mới với các cột: username, cong_viec, thoi_gian, dia_diem, luu_y
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        username TEXT,
        cong_viec TEXT,
        thoi_gian TEXT,
        dia_diem TEXT,
        luu_y TEXT
    )
''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Bảng tasks đã được tạo thành công.")
