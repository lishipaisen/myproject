import tkinter as tk
from threading import Thread
import time
from datetime import datetime
from plyer import notification
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

def create_image():
    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    d = ImageDraw.Draw(image)
    d.text((10, 10), "Water", fill=(255, 255, 255))
    return image

def show_window(icon, item):
    icon.stop()
    app.after(0, app.deiconify)

def hide_window():
    app.withdraw()
    image = create_image()
    menu = (item('Open', show_window), item('Quit', quit_app))
    icon = pystray.Icon("name", image, "Title", menu)
    icon.run()

def quit_app(icon, item):
    icon.stop()
    app.quit()

def is_time_within_range():
    now = datetime.now()
    return now.hour >= 9 and now.hour < 18

def start_timer(interval):
    t = Thread(target=remind, args=(interval,))
    t.daemon = True
    t.start()
    hide_window()  # 开始计时后隐藏主窗口

def remind(interval):
    while True:
        if is_time_within_range():
            time.sleep(interval * 60)  # 等待设置的间隔时间
            notification.notify(
                title="喝水提醒",
                message="是时候喝水了！",
                app_name="喝水提醒程序",
                timeout=10  # 通知显示时间（秒）
            )
        else:
            time.sleep(60)  # 当不在设定的时间范围内时，每分钟检查一次

app = tk.Tk()
app.title("喝水提醒程序")

label = tk.Label(app, text="设置间隔时间（分钟）:")
label.pack()

entry = tk.Entry(app)
entry.pack()

button = tk.Button(app, text="开始", command=lambda: start_timer(int(entry.get())))
button.pack()

app.protocol('WM_DELETE_WINDOW', hide_window)
app.mainloop()