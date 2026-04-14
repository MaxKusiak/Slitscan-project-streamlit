import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageTk
import tempfile
import os
import uuid
import math

def process_video(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, step, slit_scan_type, output_format) -> list:
    output_path = f"output_{uuid.uuid4()}.mp4" if output_format == "Video" else f"output_{uuid.uuid4()}.png"
    
    if os.path.exists(output_path):
        return ("File already exists. Please change the parameters to create a new output.", "error")

    # if 

    cap = cv2.VideoCapture(file_path)

    # fps = cap.get(cv2.CAP_PROP_FPS) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # file_name = file_path.split("/")[-1].replace(".mp4", "")

    v = speed

    image_width = 0
    image_height = 0
    out_frame_count = 0
    deep = 0
    senter = (round((start_x + end_x) / 2), round((start_y + end_y) / 2))
    angle = 0
    f = False
    if v == 0 or ((1 / abs(v)) >= end_frame - start_frame):
        f = True
        angle = 0
        if slit_scan_type == "Vertical":
            image_width = end_frame - start_frame
            image_height = end_y - start_y + 1
            out_frame_count = round((end_x - start_x + 1) // abs(step))
        elif slit_scan_type == "Horizontal":
            image_width = end_x - start_x + 1
            image_height = end_frame - start_frame
            out_frame_count = round((end_y - start_y + 1) // abs(step))
        elif slit_scan_type == "Circular" or slit_scan_type == "Radial":
            return ("Circular and Radial slit scan types do not support zero speed. Please change the speed to a non-zero value.", "error")
    else:
        image_width = end_x - start_x + 1
        image_height = end_y - start_y + 1
        if slit_scan_type == "Vertical":
            angle = math.atan(abs(v))
            deep = round(image_width / abs(v))
            out_frame_count = round((end_frame - start_frame + 1 - (image_width / abs(v))) / abs(step))
        elif slit_scan_type == "Horizontal":
            angle = math.atan(abs(v))
            deep = round(image_height / abs(v))
            out_frame_count = round((end_frame - start_frame + 1 - (image_height / abs(v))) / abs(step))
        elif slit_scan_type == "Circular" :
            if image_width >= image_height:
                angle = math.atan(1 / (image_height / 2))
            else:
                angle = math.atan(1 / (image_width / 2))
            deep = round((((image_width / 2) ** 2 + (image_height / 2) ** 2) ** 0.5) / abs(v))
            out_frame_count = round((end_frame - start_frame + 1 - (((((image_width / 2) ** 2 + (image_height / 2) ** 2) ** 0.5) / abs(v)))) / abs(step))
        elif slit_scan_type == "Radial":
            if image_width >= image_height:
                angle = math.atan(1 / (image_height / 2))
            else:
                angle = math.atan(1 / (image_width / 2))
            deep = round(((2 * math.pi) / angle))
            out_frame_count = round((end_frame - start_frame + 1 - ((2 * math.pi) / angle)) / abs(step))

    if output_format == "Video":
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 24, (image_width, image_height))
    else:
        out_frame_count = 1

    k = 0
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    progress.progress(0, text=f"Processing... {0}%")
    while k < out_frame_count:
        t = 0
        h1 = 0
        h2 = abs(v)
        percent = 0

        ri = 0
        r = 0
        if slit_scan_type == "Circular":
            if v < 0:
                r = (image_width ** 2 + image_height ** 2) ** 0.5 - ri * abs(v)
            else:
                r = v * ri
            # angle = math.atan(1 / r) if r != 0 else math.pi * 2

        b = 0
        j = 0
        if slit_scan_type == "Vertical":
            j = start_x - 1
            if step > 0:
                b = start_x - 1
            else:
                b = end_x - 1
        elif slit_scan_type == "Horizontal":
            j = start_y - 1

        image[:, :, :] = 0

        if not f:
            if step > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame + k * step)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame + k * step - deep + 1)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            if f:
                if slit_scan_type == "Vertical":
                    image[:, t, :] = frame[(start_y - 1):end_y, b, :]
                    t += 1
                    percent = round(t / image_width, 4)
                    if t >= image_width:
                        break
                elif slit_scan_type == "Horizontal":
                    image[t, :, :] = frame[j, (start_x - 1):end_x, :]
                    t += 1
                    percent = round(t / image_height, 4)
                    if t >= image_height:
                        break
            else:
                for i in range(round(h2) - round(h1)):
                    if slit_scan_type == "Vertical":
                        if v > 0:
                            image[:, t, :] = frame[(start_y - 1):end_y, j, :]
                        else:
                            image[:, image_width - k - 1, :] = frame[(start_y - 1):end_y, start_x - 1 + end_x - 1 - j, :]
                        j += 1
                        t += 1
                        percent = round(t / image_width, 4)
                        if t >= image_width:
                            break
                        if j >= end_x:
                            break
                    elif slit_scan_type == "Horizontal":
                        if v > 0:
                            image[t, :, :] = frame[j, (start_x - 1):end_x, :]
                        else:
                            image[image_height - t - 1, :, :] = frame[start_y - 1 + end_y - 1 - j, (start_x - 1):end_x, :]
                        j += 1
                        t += 1
                        percent = round(t / image_height, 4)
                        if t >= image_height:
                            break
                        if j >= end_y:
                            break
                    elif slit_scan_type == "Circular":
                        for a in range(round((2 * math.pi) / angle)):
                            x = round(image_width / 2) + round((r - i) * math.cos(angle * a))
                            y = round(image_height / 2) - round((r - i) * math.sin(angle * a))
                            if y >= 0 and y < image_height and x >= 0 and x < image_width:
                                image[y, x, :] = frame[senter[1] - round((r - i) * math.sin(angle * a)), senter[0] + round((r - i) * math.cos(angle * a)), :]
                        # angle = math.atan(1 / (r - i)) if (r - i) != 0 else math.pi * 2
                        # if r - i < 0:
                        #     break

                if slit_scan_type == "Vertical":
                    if t >= image_width:
                        break
                    if j >= end_x:
                        break
                elif slit_scan_type == "Horizontal":
                    if t >= image_height:
                        break
                    if j >= end_y:
                        break
                elif slit_scan_type == "Circular":
                    ri += 1
                    if v < 0:
                        r = (image_width ** 2 + image_height ** 2) ** 0.5 - ri * abs(v)
                        percent = round(1 - (r / ((image_width ** 2 + image_height ** 2) ** 0.5)), 4)
                    else:
                        r = v * ri
                        percent = round(r / ((image_width ** 2 + image_height ** 2) ** 0.5), 4)
                    # angle = math.atan(1 / r) if r != 0 else math.pi * 2

                    if v < 0:
                        if r < 0:
                            break
                    else:
                        if r > (senter[0] ** 2 + senter[1] ** 2) ** 0.5:
                            break
            h1 = h2
            h2 += abs(v)

            if output_format == "Picture":
                if percent > 1:
                    percent = 1
                progress.progress(percent, text=f"Processing... {round(percent * 100, 2)}%")

        if output_format == "Picture":
            _, buffer = cv2.imencode('.png', image)
            st.download_button(
                label="Download image",
                data=buffer.tobytes(),
                file_name=output_path,
                mime="image/png"
            )
        else:
            out.write(image)
            percent = round(k / out_frame_count, 4)
            progress.progress(percent, text=f"Processing... {percent * 100}%")
        k += 1
        b += step

    cap.release()
    if output_format == "Video":
        out.release()
    tfile.close()
    os.remove(tfile.name)
    return (output_path, "success")

st.title("Slit Scan Processor")
choose_file = st.file_uploader("Choose file", type=["mp4", "avi", "mov", "mkv"])

if choose_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(choose_file.read())
    file_path = tfile.name

    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    col1, col2 = st.columns([2, 1])

    with col2:
        slit_scan_type = st.radio("Select the type of slitscan", ["Vertical", "Horizontal", "Circular", "Radial"])
        output_format = st.selectbox("Select what you wanna get", ["Picture", "Video"])
        start_x = st.number_input(f"Start X coordinate (from 1 to {width})", min_value=1, max_value=width, value=1)
        end_x = st.number_input(f"End X coordinate (from 1 to {width} and greater than Start X)", min_value=1, max_value=width, value=width)
        start_y = st.number_input(f"Start Y coordinate (from 1 to {height})", min_value=1, max_value=height, value=1)
        end_y = st.number_input(f"End Y coordinate (from 1 to {height} and greater than Start Y)", min_value=1, max_value=height, value=height)
        speed = st.number_input("Enter speed", value=1.0)
        start_frame = st.number_input(f"Enter start frame (from 1 to {frame_count})", min_value=1, max_value=frame_count, value=1)
        end_frame = st.number_input(f"Enter end frame (from 1 to {frame_count} and greater than Start Frame)", min_value=1, max_value=frame_count, value=frame_count)
        step = st.number_input("Enter step (positive for forward processing, negative for backward processing)", value=1)
        start_processing = st.button("Start processing")

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)
        ret, frame = cap.read()

    with col1:
        st.write(f"Selected file: {choose_file.name}")
        st.write(f"Video width: {width}<br>Video height: {height}<br>Frame count: {frame_count}<br>Frame rate: {fps}", unsafe_allow_html=True)
        st.image(frame, caption="First frame of the video", channels="BGR")
        progress = st.progress(0, text="The processing progress will be displayed here")
        st.write("""Notes:<br>
                    For a radial slit, the speed parameter is not applicable.<br>
                    For a circular slit, a speed of 0 is not applicable.<br>
                    For a circular slit, it is recommended to use a speed of 0.7 or lower.<br>
                    To obtain a static vertical or horizontal slit, set the speed to 0.<br>
                    For static slits, the slit coordinate is taken from start_x or start_y.<br>
                    For static slits, the step operates not on the frame number but on the slit coordinate.""", unsafe_allow_html=True)
    
    cap.release()

    if start_processing:
        output_path = process_video(file_path, speed, start_x, end_x, start_y, end_y, start_frame, end_frame, step, slit_scan_type, output_format)
        if output_path[1] != "error":
            st.success(f"Processing completed! Output saved at: {output_path[0]}")
        else:
            st.error(output_path[0])


    # cap.release()
    # tfile.close()
    # os.remove(tfile.name)
