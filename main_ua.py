# main file 

import tkinter as tk
from tkinter import filedialog
import threading
import json
import cv2
import vertical, horizontal, circle, radian
from PIL import Image, ImageTk

CONFIG_FILE = 'config.json'
FILE_PARAMS_FILE = 'file_params.json'

# Load configuration
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save configuration
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def ask_for_folder(config):
    folder = filedialog.askdirectory(title="Оберіть папку для збереження")
    if not folder:
        tk.messagebox.showwarning("Увага", "Папку не обрано — програма не зможе зберігати файли.")
        root.destroy()
        return
    config["save_folder"] = folder
    save_config(config)
    # tk.label.config(text=f"Папка збереження:\n{folder}")
def change_folder():
    folder = filedialog.askdirectory(title="Оберіть папку для збереження")
    if folder:
        config["save_folder"] = folder
        save_config(config)
        folder_info.config(text=f"Папка збереження: {folder}")

root = tk.Tk()
root.title("Slit Scan Processor")
root.geometry("1180x600")
# root.resizable(False, False)

config = load_config()
start_x = tk.StringVar(value="1")
end_x = tk.StringVar(value="1")
start_y = tk.StringVar(value="1")
end_y = tk.StringVar(value="1")
speed = tk.StringVar(value="1.0")
step = tk.StringVar(value="1")
start_frame = tk.StringVar(value="1")
end_frame = tk.StringVar(value="0")
static_var = tk.StringVar(value="0")

if "save_folder" not in config:
    ask_for_folder(config)

# Choose file frame
choose_file_frame = tk.Frame(root, padx=10, pady=10)
choose_file_frame.grid(row=0, column=0, sticky="n")
functions = [[vertical.image, horizontal.image, circle.image, radian.image], [vertical.video, horizontal.video, circle.video]]

folder_info = tk.Label(choose_file_frame, text=f"Папка збереження: {config["save_folder"]}", wraplength=400, justify="left")
folder_info.grid(row=0, column=0, sticky="w", pady=(0,20))

change_folder_button = tk.Button(choose_file_frame, text="Змінити папку збереження", command=change_folder)
change_folder_button.grid(row=1, column=0, sticky="w", pady=(0,20))

choose_file_label = tk.Label(choose_file_frame, text=f"Обраний файл: file_name", wraplength=400, justify="left")
choose_file_info = tk.Label(choose_file_frame, text=f"Ширина відео: width\nВисота відео: height\nКількість кадрів: frame_count", wraplength=400, justify="left")
# tk.Label(choose_file_frame, text="Оберіть файл для обробки:").grid(row=1, column=0, sticky="w")

global_frame = tk.Frame(root, padx=10, pady=10)
params_frame = tk.Frame(global_frame, padx=10, pady=10)
params_frame.grid(row=0, column=0)
other_params_frame = tk.Frame(params_frame)
other_params_frame.grid(row=4, column=0, sticky="w", pady=(20,0))

# class ImageCanvas:
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.image_id = canvas.create_image(0, 0, anchor="nw")
#         self.photo = None

#     def change(self, path):
#         image = Image.open(path)
#         c = 0
#         if image.width >= image.height:
#             c = image.width / 400
#         else:
#             c = image.height / 225
#         image = image.resize((int(image.width / c), int(image.height / c)), Image.LANCZOS)
#         self.photo = ImageTk.PhotoImage(image)
#         self.canvas.itemconfig(self.image_id, image=self.photo)
#         self.canvas.coords(self.image_id, (400 - image.width) / 2, (225 - image.height) / 2)

canvas = tk.Canvas(choose_file_frame, width=400, height=225, bg="gray")
image_id = canvas.create_image(0, 0, anchor="nw")

def change_image(image_id=image_id, canvas=canvas):
    frame_index = int(start_frame.get()) - 1
    with open(FILE_PARAMS_FILE, 'r') as f:
        file_params = json.load(f)
        file_path = file_params["file_path"]
    cap = cv2.VideoCapture(file_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image1)
    c = 0
    if image.width >= image.height:
        c = image.width / 400
    else:
        c = image.height / 225
    image = image.resize((int(image.width / c), int(image.height / c)), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_id = canvas.create_image((400 - image.width) / 2, (225 - image.height) / 2, anchor="nw", image=photo)
    canvas.itemconfig(image_id, image=photo)
    canvas.coords(image_id, (400 - image.width) / 2, (225 - image.height) / 2)
    canvas.image = photo
    cap.release()

# line_id = canvas.create_line(0, 0, 0, 0)
# def draw_line(line_id=line_id, canvas=canvas):
#     canvas.delete(line_id)
#     if slitscan_type.get() == 1:
#         x = int(int(start_x.get()) / coef) + left_x
#         line_id = canvas.create_line(x, top_y, x, 225 - top_y, fill="red", width=2)
#     elif slitscan_type.get() == 2:
#         y = int(int(start_y.get()) / coef) + top_y
#         line_id = canvas.create_line(left_x, y, 400 - left_x, y, fill="red", width=2)
#     return line_id

# image_id = canvas.create_image(0, 0, anchor="nw", image=None)

# def change_image(image_path, canvas=canvas, image_id=image_id):
#     image = Image.open(image_path)
#     c = 0
#     if image.width >= image.height:
#         c = image.width / 400
#     else:
#         c = image.height / 225
#     image = image.resize((int(image.width / c), int(image.height / c)), Image.LANCZOS)
#     photo = ImageTk.PhotoImage(image)
#     canvas.itemconfig(image_id, image=photo)
#     canvas.coords(image_id, (400 - image.width) / 2, (225 - image.height) / 2)
#     canvas.image = photo

# start_x_label = None
# start_x_entry = None
# end_x_label = None
# end_x_entry = None
# start_y_label = None
# start_y_entry = None
# end_y_label = None
# end_y_entry = None
# speed_label = None
# speed_entry = None
start_frame_label = tk.Label(other_params_frame, text="")
start_frame_entry = tk.Entry(other_params_frame, textvariable=start_frame)
speed_const_label = tk.Label(other_params_frame, text="Константа для зміни швидкості:")
speed_const_entry = tk.Entry(other_params_frame, textvariable=static_var)
def choose_file():
    file_path = filedialog.askopenfilename(title="Оберіть файл для обробки", filetypes=[("Video files", "*.mp4 *.avi *.mov *.wmv")])

    if file_path:
        cap = cv2.VideoCapture(file_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        ret, frame = cap.read()
        image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image1)
        c = 0
        if image.width >= image.height:
            c = image.width / 400
        else:
            c = image.height / 225
        image = image.resize((int(image.width / c), int(image.height / c)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_id = canvas.create_image((400 - image.width) / 2, (225 - image.height) / 2, anchor="nw", image=photo)
        canvas.itemconfig(image_id, image=photo)
        canvas.coords(image_id, (400 - image.width) / 2, (225 - image.height) / 2)
        canvas.image = photo

        cap.release()

        with open(FILE_PARAMS_FILE, 'w') as f:
            json.dump({"file_path": f"{file_path}", "width": width, "height": height, "frame_count": frame_count}, f, indent=4)

        choose_button.grid(row=4, column=0, sticky="w", pady=(0,20))
        canvas.grid(row=5, column=0, sticky="nw")
        global_frame.grid(row=0, column=1, sticky="n")

        choose_file_label.config(text=f"Обраний файл: {file_path}")
        choose_file_label.grid(row=2, column=0, sticky="w", pady=(0,20))
        choose_file_info.config(text=f"Ширина відео: {width}\nВисота відео: {height}\nКількість кадрів: {frame_count}\nЧастота: {fps}")
        choose_file_info.grid(row=3, column=0, sticky="w", pady=(0,20))

        tk.Label(other_params_frame, text=f"Початкова X координата (від 1 до {width}):").grid(row=0, column=0, sticky="w")
        tk.Entry(other_params_frame, textvariable=start_x).grid(row=1, column=0, sticky="w", pady=(0,20))

        end_x.set(str(width))
        tk.Label(other_params_frame, text=f"Кінцева X координата (від 1 до {width} і більша ніж початкова):").grid(row=2, column=0, sticky="w")
        tk.Entry(other_params_frame, textvariable=end_x).grid(row=3, column=0, sticky="w", pady=(0,20))

        tk.Label(other_params_frame, text=f"Початкова Y координата (від 1 до {height}):").grid(row=0, column=1, sticky="w", padx=(20, 0))
        tk.Entry(other_params_frame, textvariable=start_y).grid(row=1, column=1, sticky="w", pady=(0,20), padx=(20, 0))

        end_y.set(str(height))
        tk.Label(other_params_frame, text=f"Кінцева Y координата (від 1 до {height} і більша ніж початкова):").grid(row=2, column=1, sticky="w", padx=(20, 0))
        tk.Entry(other_params_frame, textvariable=end_y).grid(row=3, column=1, sticky="w", pady=(0,20), padx=(20, 0))

        tk.Label(other_params_frame, text=f"Введіть швидкість:").grid(row=4, column=0, sticky="w")
        tk.Entry(other_params_frame, textvariable=speed).grid(row=5, column=0, sticky="w", pady=(0,20))

        # static_var.set("0")
        # speed_const_label.grid(row=4, column=1, sticky="w")
        # speed_const_entry.grid(row=5, column=1, sticky="w", pady=(0,20))

        start_frame.set("1")
        start_frame_label.config(text=f"Введіть початковий кадр (від 1 до {frame_count}):")
        start_frame_label.grid(row=6, column=0, sticky="w")
        start_frame_entry.grid(row=7, column=0, sticky="w", pady=(0,20))
        start_frame_entry.bind("<Return>", change_image)
        # tk.Label(other_params_frame, text=f"Введіть початковий кадр (від 1 до {frame_count}):").grid(row=6, column=0, sticky="w")
        # tk.Entry(other_params_frame, textvariable=start_frame).grid(row=7, column=0, sticky="w", pady=(0,20))
        

        complete_button.grid(row=5, column=0, sticky="w")

        end_frame_label.config(text=f"Введіть кінцевий кадр (від 1 до {frame_count} і більший ніж початковий):")
        end_frame.set(str(frame_count))
        end_frame_label.grid(row=8, column=0, sticky="w")
        end_frame_entry.grid(row=9, column=0, sticky="w", pady=(0,20))

        update_output_type()
        # tk.Scale(other_params_frame, from_=0, to=width - 1, label="Початкова X координата:", variable=start_x, orient="horizontal", length=width).grid(row=0, column=0, sticky="w")

choose_button = tk.Button(choose_file_frame, text="Обрати файл", command=choose_file)
choose_button.grid(row=2, column=0, sticky="w", pady=(0,20))

# Global frame

tk.Label(params_frame, text="Оберіть вид slitscan:", justify="left").grid(row=0, column=0, sticky="w", pady=0)

slitscan_type_frame = tk.Frame(params_frame)
slitscan_type_frame.grid(row=1, column=0, sticky="w")

def update_inputs():
    if slitscan_type.get() == 3:
        speed.set("0.7")
    else:
        speed.set("1.0")
slitscan_type = tk.IntVar(value=1)
div1 = tk.Frame(slitscan_type_frame)
div1.grid(row=0, column=0, sticky="w")
div2 = tk.Frame(slitscan_type_frame)
div2.grid(row=1, column=0)
tk.Radiobutton(div1, text="Вертикальний", variable=slitscan_type, value=1, command=update_inputs).grid(row=0, column=0, sticky="w")
tk.Radiobutton(div1, text="Горизонтальний", variable=slitscan_type, value=2, command=update_inputs).grid(row=0, column=1, sticky="w")
tk.Radiobutton(div1, text="Коловий", variable=slitscan_type, value=3, command=update_inputs).grid(row=0, column=2, sticky="w")
tk.Radiobutton(div1, text="Радіальний", variable=slitscan_type, value=4, command=update_inputs).grid(row=0, column=3, sticky="w")
# tk.Radiobutton(div2, text="Статичний горизонтальний", variable=slitscan_type, value=4, command=update_inputs).grid(row=1, column=0, sticky="w")
# tk.Radiobutton(div2, text="Статичний вертикальний", variable=slitscan_type, value=5, command=update_inputs).grid(row=1, column=1, sticky="w")

tk.Label(params_frame, text="Оберіть що ви хочете отримати:", justify="left").grid(row=2, column=0, sticky="w", pady=(20,0))

output_type_frame = tk.Frame(params_frame)
output_type_frame.grid(row=3, column=0, sticky="w")

def update_output_type():
    if output_type.get() == 2:
        # end_frame_label.grid(row=8, column=0, sticky="w")
        # end_frame_entry.grid(row=9, column=0, sticky="w", pady=(0,20))
        step_label.grid(row=10, column=0, sticky="w")
        step_entry.grid(row=11, column=0, sticky="w", pady=(0,20))
        complete_button.grid(row=6, column=0, sticky="w")
    else:
        # end_frame_label.grid_remove()
        # end_frame_entry.grid_remove()
        step_label.grid_remove()
        step_entry.grid_remove()

output_type = tk.IntVar(value=1)
tk.Radiobutton(output_type_frame, text="Картинка", variable=output_type, value=1, command=update_output_type).grid(row=0, column=0, sticky="w")
tk.Radiobutton(output_type_frame, text="Відео", variable=output_type, value=2, command=update_output_type).grid(row=0, column=1, sticky="w")

step_label = tk.Label(other_params_frame, text=f"Крок (кожен n-ний кадр буде використано):")
step_entry = tk.Entry(other_params_frame, textvariable=step)

# with open(FILE_PARAMS_FILE, 'r') as f:
#     file_params = json.load(f)
#     frame_count = file_params["frame_count"]
end_frame_label = tk.Label(other_params_frame, text=f"Введіть кінцевий кадр (від 1 до -1 і більший ніж початковий):")
end_frame_entry = tk.Entry(other_params_frame, textvariable=end_frame)
# end_frame.set(str(frame_count))

def validate_and_start():
    flag = True
    if int(start_x.get()) < 1 or int(end_x.get()) < 1:
        tk.messagebox.showerror("Помилка", "X координати не можуть бути меншими за 1.")
        flag = False
    if int(start_x.get()) >= int(end_x.get()):
        tk.messagebox.showerror("Помилка", "Початкова X координата має бути меншою за кінцеву.")
        flag = False
    if int(start_y.get()) < 1 or int(end_y.get()) < 1:
        tk.messagebox.showerror("Помилка", "Y координати не можуть бути меншими за 1.")
        flag = False
    if int(start_y.get()) >= int(end_y.get()):
        tk.messagebox.showerror("Помилка", "Початкова Y координата має бути меншою за кінцеву.")
        flag = False
    with open(FILE_PARAMS_FILE, 'r') as f:
        file_params = json.load(f)
        if int(end_x.get()) > file_params["width"]:
            tk.messagebox.showerror("Помилка", f"Кінцева X координата має бути не більшою за {file_params['width']}.")
            flag = False
        if int(start_x.get()) >= file_params["width"]:
            tk.messagebox.showerror("Помилка", f"Початкова X координата має бути меншою за {file_params['width']}.")
            flag = False
        if int(end_y.get()) > file_params["height"]:
            tk.messagebox.showerror("Помилка", f"Кінцева Y координата має бути не більшою за {file_params['height']}.")
            flag = False
        if int(start_y.get()) >= file_params["height"]:
            tk.messagebox.showerror("Помилка", f"Початкова Y координата має бути меншою за {file_params['height']}.")
            flag = False
        if int(start_frame.get()) < 1 or int(start_frame.get()) > file_params["frame_count"]:
            tk.messagebox.showerror("Помилка", f"Початковий кадр має бути в діапазоні від 1 до {file_params['frame_count']}.")
            flag = False
        # if float(speed.get()) <= 0:
        #     tk.messagebox.showerror("Помилка", "Швидкість має бути додатнім числом.")
            # flag = False
        if int(step.get()) == 0 and output_type.get() == 2:
            tk.messagebox.showerror("Помилка", "Крок не може бути нулем.")
            flag = False
        if flag:
            func = functions[output_type.get() - 1][slitscan_type.get() - 1]
            threading.Thread(target=func, args=(file_params["file_path"], float(speed.get()), int(start_x.get()) - 1, int(end_x.get()) - 1, int(start_y.get()) - 1, int(end_y.get()) - 1, int(start_frame.get()) - 1, int(end_frame.get()), config["save_folder"], float(static_var.get())) if output_type.get() == 1 else (file_params["file_path"], float(speed.get()), int(start_x.get()) - 1, int(end_x.get()) - 1, int(start_y.get()) - 1, int(end_y.get()) - 1, int(start_frame.get()) - 1, int(end_frame.get()), config["save_folder"], int(step.get())), daemon=True).start()
            # func(file_params["file_path"], float(speed.get()), int(start_x.get()), int(end_x.get()), int(start_frame.get()) - 1, config["save_folder"]) if output_type.get() == 1 else func(file_params["file_path"], float(speed.get()), int(start_x.get()), int(end_x.get()), int(start_frame.get()) - 1, config["save_folder"], int(step.get()))
            # tk.messagebox.showinfo("Готово", "Обробка завершена!")

complete_button = tk.Button(params_frame, text="Почати обробку", command=validate_and_start)

static_label = tk.Label(other_params_frame, text="")
static_entry = tk.Entry(other_params_frame, textvariable=static_var)

# def advanced_options():
#     pass
# tk.Button(params_frame, text="Далі", command=advanced_options).grid(row=4, column=0, sticky="w", pady=(20,0))

root.mainloop()


# file_name = input("Enter file name: ")
# speed = float(input("Enter speed (not used in current version): "))
# step = int(input("Enter step size: "))
# start_x = int(input("Enter start x coordinate or enter -1: "))
# end_x = int(input("Enter end x coordinate or enter -1: "))
# start_frame = int(input("Enter start frame or enter 0: "))
# choice = int(input("Choose pattern - 1: Vertical, 2: Horizontal, 3: Circle: "))
# isImage = input("Do you want image or video? (i - image/v - video): ").lower()

# if isImage == 'i':
#     if choice == 1:
#         vertical.image(file_name, speed, start_x, end_x, start_frame)
#     elif choice == 2:
#         gorizontal.image(file_name, speed, start_x, end_x, start_frame)
#     elif choice == 3:
#         circle.image(file_name, speed, start_x, end_x, start_frame)
#     else:
#         print("Invalid choice")
# elif isImage == 'v':
#     if choice == 1:
#         vertical.video(file_name, speed, step, start_x, end_x, start_frame)
#     elif choice == 2:
#         gorizontal.video(file_name, speed, step, start_x, end_x, start_frame)
#     elif choice == 3:
#         circle.video(file_name, speed, step, start_x, end_x, start_frame)
#     else:
#         print("Invalid choice")
# else:
#     print("Invalid input")
# vertical.image("mars", 0.5, 0, 1083, 100)
# gorizontal.video("panorama", 5, 1, -1, -1, 0)
