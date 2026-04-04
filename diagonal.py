import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import ttk
import math as Math

def image(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, download_folder, speed_const, angle = 15):
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    file_name = file_path.split("/")[-1].replace(".mp4", "")

    v = lambda time, speed=speed, speed_const=speed_const: speed + speed_const * (time ** 2)
    # if start_x == -1:
    #     start_x = 0
    # if end_x == -1:
    #     end_x = width - 1

    if os.path.exists(f'{download_folder}/{file_name}-slitscan_diag-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-angle_{angle}.png'):
        # print("file already exists")
        tk.messagebox.showerror("Помилка", "Файл вже існує.")
        return

    # image_width = 0
    # image_height = end_y - start_y + 1
    # h1 = 0
    # h2 = abs(v(0))
    # j = start_x
    # f = False
    # if v(0) == 0 or abs(1 / v(0)) >= end_frame - start_frame:
    #     f = True
    #     image_width = end_frame - start_frame
    #     image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    # else:
    #     image_width = end_x - start_x + 1
    #     image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    # if direction == "up":
    #     image = np.zeros((end_frame - start_frame, width, 3), dtype=np.uint8)
    # else:
    image = np.zeros((height, end_frame - start_frame, 3), dtype=np.uint8)

    win = tk.Tk()
    win.title("Processing...")
    win.geometry("300x50")

    lablel = tk.Label(win, text="Processing... 0.0%")
    lablel.grid(row=0, column=0, padx=10, pady=5)

    bar = ttk.Progressbar(win, length=280, mode='determinate', maximum=100)
    bar.grid(row=1, column=0, padx=10, pady=5)
    bar['value'] = 0
    win.update()

    k = 0
    phi = angle * (Math.pi / 180)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if k >= end_frame - start_frame:
            break
        # if direction == "up":
        # for w in range(round(width / Math.cos(phi))):
        #     try:
        #         image[k, w, :] = frame[end_y - abs(round(w * Math.tan(phi))), w, :]
        #     except:
        #         pass
        # else:
        for h in range(height):
            try:
                image[height - h - 1, k, :] = frame[height - h - 1, abs(round(h / Math.tan(phi))), :]
            except:
                pass

        k += 1

    cv2.imwrite(f'{download_folder}/{file_name}-slitscan_diag-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-angle_{angle}.png', image)

    cap.release()
    
    win.destroy()
    # tk.messagebox.showinfo("Готово", f"Обробка завершена! Файл збережено як {file_name}-slitscan_diag-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-angle_{angle}.png")
    
    # h, w = image.shape[:2]
    # scale = min(960 / w, 540 / h)
    # resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    # cv2.imshow("Result", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.startfile(f'{download_folder}/{file_name}-slitscan_diag-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-angle_{angle}.png')

image("C:/Users/maxku/Downloads/MAN/mars.mp4", 1.0, 0, 1083, 0, 719, 0, 1843, "C:/Users/maxku/Downloads/MAN", 0.0)
