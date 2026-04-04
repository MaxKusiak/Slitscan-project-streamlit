# Slit-scan circle effect, video

import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import ttk

def video(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, download_folder, step):
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    file_name = file_path.split("/")[-1].replace(".mp4", "")

    v = speed
    # if frame_count > height / 2 + 100:
    #     v = 0.7
    # else:
    #     print(f"frame count error\nframe_count: {frame_count}\nheight: {height}\nerror result: {height / 2 + 100}")
    #     return
    # if start_x == -1:
    #     start_x = 0
    # if end_x == -1:
    #     end_x = width - 1

    if os.path.exists(f'{download_folder}/{file_name}-slitscan_circle-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4'):
        tk.messagebox.showerror("Error", "File already exists.")
        return

    image_width = end_x - start_x + 1
    image_height = end_y - start_y + 1

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{download_folder}/{file_name}-slitscan_circle-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4', fourcc, 24, (image_width, image_height))

    senter = (round(image_width / 2), round(image_height / 2))
    r = v

    # print(round((end_frame - start_frame - ((((senter[0] ** 2 + senter[1] ** 2) ** 0.5) / abs(v)) + 1)) / abs(step)))
    # exit()
    m = []
    for i in range(round((end_frame - start_frame - ((((senter[0] ** 2 + senter[1] ** 2) ** 0.5) / abs(v)) + 1)) / abs(step))):
        m.append(np.zeros((image_height, image_width, 3), dtype=np.uint8))

    win = tk.Tk()
    win.title("Processing...")
    win.geometry("300x70")

    label = tk.Label(win, text="Processing... 0.0%")
    label.grid(row=0, column=0, padx=10, pady=5)

    bar = ttk.Progressbar(win, length=280, mode='determinate', maximum=100)
    bar.grid(row=1, column=0, padx=10, pady=5)
    bar['value'] = 0
    win.update()

    ri = 0
    k = 0
    while k < len(m):

        image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

        ri = 0
        r = v

        if step > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + k * step)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame + k * step - round(((senter[0] ** 2 + senter[1] ** 2) ** 0.5) / abs(v)) + 1)
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            r = v * ri

            for j in range(round(image_height / 2)):
                try:
                    if j + senter[1] < image_height and round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] < image_width:
                        image[j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
                    if j + senter[1] < image_height and (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] >= start_x:
                        image[j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) - senter[0], :]
                    if (-1) * j + senter[1] >= 0 and round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] < image_width:
                        image[(-1) * j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[(-1) * j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
                    if (-1) * j + senter[1] >= 0 and (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] >= start_x:
                        image[(-1) * j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[(-1) * j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
                except:
                    pass

            for i in range(round(image_width / 2)):
                try:
                    if round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] < image_height and i + senter[0] < image_width:
                        image[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :] = frame[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :]
                    if round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] < image_height and (-1) * i + senter[0] >= start_x:
                        image[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :] = frame[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :]
                    if (-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] >= 0 and i + senter[0] < image_width:
                        image[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :] = frame[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :]
                    if (-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] >= 0 and (-1) * i + senter[0] >= start_x:
                        image[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :] = frame[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :]
                except:
                    pass
            
            ri += 1

            if r > (senter[0] ** 2 + senter[1] ** 2) ** 0.5:
                break
            
        m[k] = image
        k += 1

        label.config(text=f"Processing... {round((k * 100) / len(m), 2)}%")
        bar['value'] = round((k * 100) / len(m), 2)
        win.update()
        # print(round((k * 100) / len(m), 2), "%")

    for i in range(len(m)):
        out.write(m[i])

    cap.release()
    out.release()

    win.destroy()
    tk.messagebox.showinfo("Done", f"Processing complete! File saved as {file_name}-slitscan_circle-speed_{v}-startx_{start_x}-endx_{end_x}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4")

    os.startfile(f'{download_folder}/{file_name}-slitscan_circle-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4')

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
    
    if os.path.exists(f'{download_folder}/{file_name}-slitscan_circle-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png'):
        tk.messagebox.showerror("Error", "File already exists.")
        return

    ri = 0
    # r1 = 0
    # r2 = v
    r = 0
    image_width = end_x - start_x + 1
    image_height = end_y - start_y + 1
    senter = (round(image_width / 2), round(image_height / 2))
    senter2 = (senter[0] + start_x, senter[1] + start_y)
    if v(0) < 0:
        r = (senter[0] ** 2 + senter[1] ** 2) ** 0.5

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

    # k = 0
    n = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.isOpened():
        # cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + k * step)
        ret, frame = cap.read()

        if not ret:
            break
        
        n = cap.get(cv2.CAP_PROP_POS_FRAMES) - start_frame + 1

        if v(n) < 0:
            r = (senter[0] ** 2 + senter[1] ** 2) ** 0.5 - ri * abs(v(n))
        else:
            r = v(n) * ri

        # for t in range(round(r2) - round(r1)):
        for j in range(round(image_height / 2)):
            try:
                if j + senter[1] < image_height and round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] < image_width:
                    image[j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
                if j + senter[1] < image_height and (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] >= start_x:
                    image[j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) - senter[0], :]
                if (-1) * j + senter[1] >= 0 and round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] < image_width:
                    image[(-1) * j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[(-1) * j + senter[1], round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
                if (-1) * j + senter[1] >= 0 and (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0] >= start_x:
                    image[(-1) * j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :] = frame[(-1) * j + senter[1], (-1) * round(((r ** 2) - (j ** 2)) ** 0.5) + senter[0], :]
            except:
                pass
            
        for i in range(round(image_width / 2)):
            try:
                if round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] < image_height and i + senter[0] < image_width:
                    image[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :] = frame[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :]
                if round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] < image_height and (-1) * i + senter[0] >= start_x:
                    image[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :] = frame[round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :]
                if (-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] >= 0 and i + senter[0] < image_width:
                    image[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :] = frame[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], i + senter[0], :]
                if (-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1] >= 0 and (-1) * i + senter[0] >= start_x:
                    image[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :] = frame[(-1) * round(((r ** 2) - (i ** 2)) ** 0.5) + senter[1], (-1) * i + senter[0], :]
            except:
                pass
            # r += 1
        
        ri += 1
        # r1 = r2
        # r2 += v
    
        if v(n) < 0:
            if r < 0:
                break
        else:
            if r > (senter[0] ** 2 + senter[1] ** 2) ** 0.5:
                break

        label.config(text=f"Processing... {round((r * 100) / ((senter[0] ** 2 + senter[1] ** 2) ** 0.5), 2)}%")
        bar['value'] = round((r * 100) / ((senter[0] ** 2 + senter[1] ** 2) ** 0.5), 2)
        win.update()
        
    cv2.imwrite(f'{download_folder}/{file_name}-slitscan_circle-speed_{speed}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png', image)

    cap.release()
    
    tk.messagebox.showinfo("Done", f"Processing complete! File saved as {file_name}-slitscan_circle-speed_{speed}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png")

    # h, w = image.shape[:2]
    # scale = min(960 / w, 540 / h)
    # resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    # cv2.imshow("Result", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.startfile(f'{download_folder}/{file_name}-slitscan_circle-speed_{speed}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png')
