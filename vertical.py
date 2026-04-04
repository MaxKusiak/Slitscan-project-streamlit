# варіант №1. нарізає збоку на нові кадри
# перероблено під v2

import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def video(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, download_folder, step):
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    file_name = file_path.split("/")[-1].replace(".mp4", "")

    v = speed
    # if start_x == -1:
    #     start_x = 0
    # if end_x == -1:
    #     end_x = width - 1
    # if frame_count > end_x - start_x + 1 + 100:
    #     v = 1
    # else:
    #     print(f"frame count error\nframe_count: {frame_count}\nwidth: {end_x - start_x + 1}\nerror result: {end_x - start_x + 1 + 100}")
    #     return
    
    if os.path.exists(f'{download_folder}/{file_name}-slitscan_v1-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4'):
        tk.messagebox.showerror("Error", "File already exists.")
        return
    
    image_width = 0
    image_height = end_y - start_y + 1
    out_frame_count = 0
    f = False
    m = []
    if v == 0 or ((1 / abs(v)) >= end_frame - start_frame):
        f = True
        image_width = end_frame - start_frame
        out_frame_count = round((end_x - start_x + 1) // abs(step))
        # for i in range(round((end_x - start_x + 1) // abs(step))):
        #     m.append(np.zeros((image_height, image_width, 3), dtype=np.uint8))
    else:
        image_width = end_x - start_x + 1
        out_frame_count = round((end_frame - start_frame + 1 - (image_width / abs(v))) / abs(step))
        # for i in range(round((end_frame - start_frame + 1 - (image_width / abs(v))) / abs(step))):
        #     m.append(np.zeros((image_height, image_width, 3), dtype=np.uint8))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')   
    out = cv2.VideoWriter(f'{download_folder}/{file_name}-slitscan_v1-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4', fourcc, 24, (image_width, image_height))

    win = tk.Tk()
    win.title("Processing...")
    win.geometry("300x70")

    label = tk.Label(win, text="Processing... 0.0%")
    label.grid(row=0, column=0, padx=10, pady=5)

    bar = ttk.Progressbar(win, length=280, mode='determinate', maximum=100)
    bar.grid(row=1, column=0, padx=10, pady=5)
    bar['value'] = 0
    win.update()

    k = 0
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    if step > 0:
        b = start_x
    else:
        b = end_x
    while k < out_frame_count:
        t = 0
        h1 = 0
        h2 = abs(v)
        j = start_x
        image[:, :, :] = 0

        if not f:
            if step > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + k * step)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame + k * step - round(image_width / abs(v)) + 1)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            
            if f:
                image[:, t, :] = frame[start_y:end_y + 1, b, :]

                t += 1
                if t >= image_width:
                    break
            else:
                # if v > 0:
                #     image[:, t, :] = frame[start_y:end_y + 1, j, :]
                # else:
                #     image[:, image_width - k - 1, :] = frame[start_y:end_y + 1, start_x + end_x - j, :]
                # t += 1
                # if t >= image_width:
                #     break

                # if not (round(h2) - round(h1) == 0):
                #     j += 1
                #     if j >= end_x + 1:
                #         break
                
                for i in range(round(h2) - round(h1)):
                    if v > 0:
                        image[:, t, :] = frame[start_y:end_y + 1, j, :]
                    else:
                        image[:, image_width - k - 1, :] = frame[start_y:end_y + 1, start_x + end_x - j, :]
                    j += 1
                    t += 1
                    if t >= image_width:
                        break
                    if j >= end_x + 1:
                        break

                if t >= image_width:
                    break
                if j >= end_x + 1:
                    break
            # if j >= end_x + 1:
            #     break
            # if t >= image_width:
            #     break
            
            # if f:
            #     image[:, t, :] = frame[start_y:end_y + 1, b, :]
            #     # p = start_x
            #     # while p < end_x - start_x + 1:
            #     #     for i in range(len(m)):
            #     #         m[i][:, t, :] = frame[:, p, :]
            #     #     p += 1
            #     t += 1
            #     if t >= image_width:
            #         break
            # else:
            #     for i in range(round(h2) - round(h1)):
            #         if v > 0:
            #             image[:, t, :] = frame[start_y:end_y + 1, j, :]
            #         else:
            #             image[:, t, :] = frame[start_y:end_y + 1, end_x - 1 - j, :]
            #         j += 1
            #         t += 1
            #         if j >= end_x + 1:
            #             break
            #         if t >= image_width:
            #             break
            
            # label.config(text=f"Processing... {round((t * 100) / image_width, 2)}%")
            # bar['value'] = round((t * 100) / image_width, 2)
            # win.update()
            h1 = h2
            h2 += abs(v)

        # m[k] = image
        out.write(image)
        k += 1
        b += step

        label.config(text=f"Processing... {round((k * 100) / out_frame_count, 2)}%")
        bar['value'] = round((k * 100) / out_frame_count, 2)
        win.update()
        # print(round((k * 100) / len(m), 2), "%")

    # cv2.imwrite(f'{download_folder}/{file_name}-slitscan_v1-speed_{v}-startx_{start_x}-endx_{end_x}-startframe_{start_frame}-endframe_{end_frame}.png', m[len(m) - 1])
    # win.destroy()
    # exit()
    # for i in range(len(m)):
    #     out.write(m[i])

    cap.release()
    out.release()

    win.destroy()
    tk.messagebox.showinfo("Done", f"Processing complete! File saved as {file_name}-slitscan_v1-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4")

    os.startfile(f'{download_folder}/{file_name}-slitscan_v1-speed_{v}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}-step_{step}.mp4')

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

    if os.path.exists(f'{download_folder}/{file_name}-slitscan_v1-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png'):
        # print("file already exists")
        tk.messagebox.showerror("Error", "File already exists.")
        return

    image_width = 0
    image_height = end_y - start_y + 1
    h1 = 0
    h2 = abs(v(0))
    j = start_x
    f = False
    if v(0) == 0 or abs(1 / v(0)) >= end_frame - start_frame:
        f = True
        image_width = end_frame - start_frame
        image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    else:
        image_width = end_x - start_x + 1
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

    k = 0
    n = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        n = cap.get(cv2.CAP_PROP_POS_FRAMES) - start_frame + 1
        # if j >= end_x:
        #     break
        # if k >= image_width:
        #     break

        if f:
            image[:, k, :] = frame[start_y:end_y + 1, j, :]

            label.config(text=f"Processing... {round((k * 100) / image_width, 2)}%")
            bar['value'] = round((k * 100) / image_width, 2)
            win.update()
            k += 1
            if k >= image_width:
                break
        else:
            # if v > 0:
            #     image[:, k, :] = frame[start_y:end_y + 1, j, :]
            # else:
            #     image[:, image_width - k - 1, :] = frame[start_y:end_y + 1, start_x + end_x - j, :]
            # k += 1
            # if k >= image_width:
            #     break    
            # label.config(text=f"Processing... {round((k * 100) / image_width, 2)}%")
            # bar['value'] = round((k * 100) / image_width, 2)
            # win.update()

            # if not (round(h2) - round(h1) == 0):
            #     j += 1
            #     if j >= end_x + 1:
            #         break
            
            for i in range(round(h2) - round(h1)):
                if v(n) > 0:
                    image[:, k, :] = frame[start_y:end_y + 1, j, :]
                else:
                    image[:, image_width - k - 1, :] = frame[start_y:end_y + 1, start_x + end_x - j, :]
                j += 1
                k += 1
                if k >= image_width:
                    break
                if j >= end_x + 1:
                    break

                label.config(text=f"Processing... {round((k * 100) / image_width, 2)}%")
                bar['value'] = round((k * 100) / image_width, 2)
                win.update()
            if k >= image_width:
                break
            if j >= end_x + 1:
                break

        h1 = h2
        h2 += abs(v(n))

    cv2.imwrite(f'{download_folder}/{file_name}-slitscan_v1-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png', image)

    cap.release()
    
    win.destroy()
    tk.messagebox.showinfo("Done", f"Processing complete! File saved as {file_name}-slitscan_v1-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png")
    
    # h, w = image.shape[:2]
    # scale = min(960 / w, 540 / h)
    # resized = cv2.resize(image, (int(w * scale), int(h * scale)))
    # cv2.imshow("Result", resized)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.startfile(f'{download_folder}/{file_name}-slitscan_v1-speed_{v(0)}-startx_{start_x}-endx_{end_x}-starty_{start_y}-endy_{end_y}-startframe_{start_frame}-endframe_{end_frame}.png')
