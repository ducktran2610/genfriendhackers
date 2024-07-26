import tkinter as tk
from tkinter import Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path
import threading
import speech_recognition as sr
from gtts import gTTS
import playsound
import requests
import json
import os
import sqlite3
from datetime import datetime



# Kết nối tới database
db = sqlite3.connect('data.db')
cursor = db.cursor()
username = 'TranDuck'

API_URL = "https://api.coze.com/open_api/v2/chat"
psn_token = "pat_NyD4nlGvOto9c7OoSISO6x3uqQhgN0oO3rtNewgdvpXNw9RZk7FHjNFHT2oFa4nR"
header = {
    "Authorization": f'Bearer {psn_token}',
    "Content-type": 'application/json',
    'Connection': "keep-alive",
    "Accept": "*/*",
}
cursor.execute("SELECT history_chat FROM users WHERE username = ?", (username,))
row = cursor.fetchone()
if row:
    history_chat = row[0]
    history = json.loads(history_chat)
else:
    history = []
print(history)
data2 = {
    "conservation_id": "demo-0",
    "bot_id": "7377038220523700242",
    "user": "demo-user",
    "query": "2 + 2 bằng mấy",
    "stream": False,
    "chat_history": history,
}

def rating():
    vote_point = 0
    def vote_point_u(a):
        global vote_point
        vote_point = a
    def sumbit():
        global vote_point
        # Lấy thời gian hiện tại
        now = datetime.now()

        # Định dạng thời gian theo cách bạn muốn
        formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO rating (time, point, username) VALUES (?, ?, ?)",(formatted_now, vote_point, username))
        db.commit()
        rating_window.destroy()
    rating_window = tk.Toplevel(window)
    rating_window.geometry("800x450")
    rating_window.configure(bg="#3A5184")

    canvas = Canvas(
        rating_window,
        bg="#3A5184",
        height=450,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    rating_sumbit_img = PhotoImage(file=relative_to_assets("rating_sumbit_img.png"))
    rating_sumbit_button = Button(
        rating_window,
        image=rating_sumbit_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: sumbit(),
        relief="flat",
        activebackground="#3A5284"
    )
    rating_sumbit_button.place(
        x=323.0,
        y=381.0,
        width=153.0,
        height=46.0
    )

    canvas.create_rectangle(
        160.0,
        160.0,
        656.0,
        286.0,
        fill="#FFFFFF",
        outline=""
    )

    canvas.create_rectangle(
        127.0,
        56.0,
        673.0,
        347.0,
        fill="#FFFFFF",
        outline=""
    )

    canvas.create_text(
        198.0,
        358.0,
        anchor="nw",
        text="Bạn có thể góp ý để trải nghiệm lần tới được tốt hơn!",
        fill="#FFFFFF",
        font=("Inter SemiBoldItalic", 16 * -1)
    )

    rating_vote_1_img = PhotoImage(file=relative_to_assets("vote_1_img.png"))
    rating_vote_1_button = Button(
        rating_window,
        image=rating_vote_1_img,
        borderwidth=0,
        highlightthickness=0,
        command= lambda: vote_point_u(1),
        relief="flat",
        activebackground="#FFFFFF"
    )
    rating_vote_1_button.place(
        x=570.0,
        y=173.0,
        width=58.0,
        height=88.0
    )

    rating_vote_3_img = PhotoImage(file=relative_to_assets("vote_3_img.png"))
    rating_vote_3_button = Button(
        rating_window,
        image=rating_vote_3_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vote_point_u(3),
        relief="flat",
        activebackground="#FFFFFF"
    )
    rating_vote_3_button.place(
        x=367.0,
        y=173.0,
        width=85.0,
        height=92.0
    )

    rating_vote_2_img = PhotoImage(file=relative_to_assets("vote_2_img.png"))
    rating_vote_2_button = Button(
        rating_window,
        image=rating_vote_2_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vote_point_u(2),
        relief="flat",
        activebackground="#FFFFFF"
    )
    rating_vote_2_button.place(
        x=481.0,
        y=170.0,
        width=60.0,
        height=103.0
    )

    rating_vote_4_img = PhotoImage(file=relative_to_assets("vote_4_img.png"))
    rating_vote_4_button = Button(
        rating_window,
        image=rating_vote_4_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vote_point_u(4),
        relief="flat",
        activebackground="#FFFFFF"
    )
    rating_vote_4_button.place(
        x=277.0,
        y=175.0,
        width=60.0,
        height=86.0
    )

    rating_vote_5_img = PhotoImage(file=relative_to_assets("vote_5_img.png"))
    rating_vote_5_button = Button(
        rating_window,
        image=rating_vote_5_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vote_point_u(5),
        relief="flat",
        activebackground="#FFFFFF"
    )
    rating_vote_5_button.place(
        x=172.0,
        y=173.0,
        width=65.0,
        height=86.0
    )

    canvas.create_text(
        185.0,
        129.0,
        anchor="nw",
        text="MỨC ĐỘ HÀI LÒNG CỦA BẠN VỀ SẢN PHẨM",
        fill="#000000",
        font=("Inter BoldItalic", 20 * -1)
    )
    rating_window.resizable(False, False)
    rating_window.mainloop()

def say(text, lang='vi'):
    def run():
        tts = gTTS(text=text, lang=lang)
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

    threading.Thread(target=run).start()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        main_anou_text.delete("1.0", tk.END)
        main_anou_text.insert(tk.END, "Hãy nói điều gì đó...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        main_anou_text.delete("1.0", tk.END)
        main_anou_text.insert(tk.END, "Ghi nhận giọng nói thành công")
        main_input_entry.delete(0, tk.END)
        main_input_entry.insert(0, text)
    except sr.UnknownValueError:
        main_anou_text.delete("1.0", tk.END)
        main_anou_text.insert(tk.END, "Google Speech Recognition không thể nhận dạng giọng nói")
    except sr.RequestError as e:
        main_anou_text.delete("1.0", tk.END)
        main_anou_text.insert(tk.END, f"Không thể yêu cầu kết quả từ Google Speech Recognition; {e}")

def send_data():
    text = main_input_entry.get().strip()
    main_output_text.config(state=tk.NORMAL)
    main_output_text.insert(tk.END, "Bạn: " + text + "\n")
    main_output_text.config(state=tk.DISABLED)
    if text:
        data2["query"] = text
        data = json.dumps(data2)
        main_anou_text.delete("1.0", tk.END)
        main_anou_text.insert(tk.END, "Đang chờ AI phản hồi...")

        res = requests.post(API_URL, data=data, headers=header)

        if res.status_code == 200:
            Ai_ans = [ans['content'] for ans in res.json()['messages'] if ans['type'] == "answer"]
            main_output_text.config(state=tk.NORMAL)
            main_output_text.insert(tk.END, "GenFriend: " + Ai_ans[0] + "\n")
            main_output_text.config(state=tk.DISABLED)
            say(Ai_ans[0])
            user = {
                "role": "user",
                "content": text,
                "content_type": "text"
            }
            bot = {
                "role": "assistant",
                "type": "answer",
                "content": Ai_ans[0],
                "content_type": "text"
            }
            history.extend([user, bot])
            data2["chat_history"] = history
            updated_history_json = json.dumps(history)
            cursor.execute("UPDATE users SET history_chat = ? WHERE username = ?", (updated_history_json, username))
            db.commit()
        else:
            main_anou_text.delete("1.0", tk.END)
            main_anou_text.insert(tk.END, f"Yêu cầu API thất bại với mã trạng thái: {res.status_code}")

def start_recognition_thread():
    recognition_thread = threading.Thread(target=recognize_speech)
    recognition_thread.start()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\python\bot\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = tk.Tk()
window.geometry("800x450")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=450,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

main_input_entry_img = PhotoImage(file=relative_to_assets("main_input_entry_img.png"))
main_input_bg = canvas.create_image(337.5, 407.0, image=main_input_entry_img)
main_input_entry = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
main_input_entry.place(x=65.0, y=392.0, width=545.0, height=28.0)

main_send_button_img = PhotoImage(file=relative_to_assets("main_send_button_img.png"))
main_send_button = Button(
    image=main_send_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=send_data,
    relief="flat"
)
main_send_button.place(x=656.0, y=390.0, width=33.0, height=33.0)

main_voice_button_img = PhotoImage(file=relative_to_assets("main_voice_button_img.png"))
main_voice_button = Button(
    image=main_voice_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=start_recognition_thread,
    relief="flat"
)
main_voice_button.place(x=712.0, y=390.0, width=33.0, height=33.0)

main_log_button_img = PhotoImage(
    file=relative_to_assets("main_log_button.png"))
main_log_button = Button(
    image=main_log_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
main_log_button.place(
    x=712.0,
    y=346.0,
    width=33.0,
    height=33.0
)

main_rating_button_img = PhotoImage(
    file=relative_to_assets("main_rating_button.png"))
main_rating_button = Button(
    image=main_rating_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=rating,
    relief="flat"
)
main_rating_button.place(
    x=656.0,
    y=346.0,
    width=33.0,
    height=33.0
)

main_output_text_img = PhotoImage(file=relative_to_assets("main_output_text_img.png"))
main_output_bg = canvas.create_image(400.0, 177.0, image=main_output_text_img)
main_output_text = Text(bd=0, bg="#6ACCEB", fg="#000716", highlightthickness=0)
main_output_text.place(x=74.0, y=27.0, width=652.0, height=298.0)
main_output_text.config(state=tk.DISABLED)

main_anou_text_img = PhotoImage(file=relative_to_assets("main_anou_text_img.png"))
main_anou_bg = canvas.create_image(399.5, 359.5, image=main_anou_text_img)
main_anou_text = Text(bd=0, bg="#A1F3FF", fg="#000716", highlightthickness=0)
main_anou_text.place(x=250.0, y=346.0, width=299.0, height=25.0)

window.resizable(False, False)
window.mainloop()
