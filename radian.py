import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import ttk
import math as Math

def image(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, download_folder, speed_const):
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
    
    if os.path.exists(f'{download_folder}/{file_name}-slitscan_rad-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png'):
        # print("file already exists")
        tk.messagebox.showerror("Error", "File already exists.")
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
    image_width = end_x - start_x + 1
    image_height = end_y - start_y + 1
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    win = tk.Tk()
    win.title("Processing...")
    win.geometry("300x70")

    label = tk.Label(win, text="Processing... 0.0%")
    label.grid(row=0, column=0, padx=10, pady=5)

    bar = ttk.Progressbar(win, length=280, mode='determinate', maximum=100)
    bar.grid(row=1, column=0, padx=10, pady=5)
    bar['value'] = 0
    win.update()

    g_senter = (start_x + (end_x - start_x + 1) // 2, start_y + (end_y - start_y + 1) // 2)
    senter = (image_width // 2, image_height // 2)

    phi = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
            
        if phi > Math.pi * 2:
            break

        for l in range(round((((image_width / 2) ** 2) + ((image_height / 2) ** 2)) ** 0.5)):
            h = senter[1] - round(l * Math.sin(phi))
            w = senter[0] + round(l * Math.cos(phi))
            if h >= 0 and h < image_height and w >= 0 and w < image_width:
                image[h, w, :] = frame[g_senter[1] - round(l * Math.sin(phi)), g_senter[0] + round(l * Math.cos(phi)), :]

        # if phi >= 0 and phi < Math.pi / 2:
        #     # I quarter
        #     for l in range(round((((image_width / 2) ** 2) + ((image_height / 2) ** 2)) ** 0.5)):
        #         if senter[1] - abs(round(l * Math.sin(phi))) >= 0 and senter[0] + abs(round(l * Math.cos(phi))) < image_width:
        #             image[senter[1] - abs(round(l * Math.sin(phi))), senter[0] + abs(round(l * Math.cos(phi))), :] = frame[g_senter[1] - abs(round(l * Math.sin(phi))), g_senter[0] + abs(round(l * Math.cos(phi))), :]
        # elif phi >= Math.pi / 2 and phi < Math.pi:
        #     # II quarter
        #     for l in range(round((((image_width / 2) ** 2) + ((image_height / 2) ** 2)) ** 0.5)):
        #         if senter[1] - abs(round(l * Math.sin(phi))) >= 0 and senter[0] - abs(round(l * Math.cos(phi))) >= 0:
        #             image[senter[1] - abs(round(l * Math.sin(phi))), senter[0] - abs(round(l * Math.cos(phi))), :] = frame[g_senter[1] - abs(round(l * Math.sin(phi))), g_senter[0] - abs(round(l * Math.cos(phi))), :]
        # elif phi >= Math.pi and phi < Math.pi * 1.5:
        #     # III quarter
        #     for l in range(round((((image_width / 2) ** 2) + ((image_height / 2) ** 2)) ** 0.5)):
        #         if senter[1] + abs(round(l * Math.sin(phi))) < image_height and senter[0] - abs(round(l * Math.cos(phi))) >= 0:
        #             image[senter[1] + abs(round(l * Math.sin(phi))), senter[0] - abs(round(l * Math.cos(phi))), :] = frame[g_senter[1] + abs(round(l * Math.sin(phi))), g_senter[0] - abs(round(l * Math.cos(phi))), :]
        # else:
        #     # IV quarter
        #     for l in range(round((((image_width / 2) ** 2) + ((image_height / 2) ** 2)) ** 0.5)):
        #         if senter[1] + abs(round(l * Math.sin(phi))) < image_height and senter[0] + abs(round(l * Math.cos(phi))) < image_width:
        #             image[senter[1] + abs(round(l * Math.sin(phi))), senter[0] + abs(round(l * Math.cos(phi))), :] = frame[g_senter[1] + abs(round(l * Math.sin(phi))), g_senter[0] + abs(round(l * Math.cos(phi))), :]

        label.config(text=f"Processing... {round((phi / (Math.pi * 2)) * 100, 2)}%")
        bar['value'] = round((phi / (Math.pi * 2)) * 100, 2)
        win.update()

        phi += Math.pi / 1650

    cv2.imwrite(f'{download_folder}/{file_name}-slitscan_rad-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png', image)

    cap.release()
    
    win.destroy()
    tk.messagebox.showinfo("Done", f"Processing complete! File saved as {file_name}-slitscan_rad-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png")
    
    # h, w = image.shape[:2]
    # scale = min(960 / w, 540 / h)
    # resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    # cv2.imshow("Result", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.startfile(f'{download_folder}/{file_name}-slitscan_rad-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png')

# image("C:/Users/maxku/Downloads/MAN/mars.mp4", 1.0, 0, 1279, 0, 719, 0, 3588, "C:/Users/maxku/Downloads/MAN", 0.0)
