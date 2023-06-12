import tkinter as tk
import os
from tkinter import filedialog, messagebox
from tkinter import *

dict_sn_save = {}
nms = 3


class MyDialog:
    def __init__(self, parent, valor, title):
        self.valor = valor

        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg="#EFEFEF")
        # self.top.iconbitmap("icon/beer.ico")
        if len(title) > 0: self.top.title(title)
        self.nms_lb = tk.Label(self.top, text="Số bản ghi  ", bg="#EFEFEF", bd=10)
        self.nms_lb.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.nms_entry = tk.Entry(self.top, bg="#EFEFEF", width=10)
        self.nms_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.pass_lb = tk.Label(self.top, text="Password  ", bg="#EFEFEF", bd=10)
        self.pass_lb.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.pass_entry = tk.Entry(self.top, bg="#EFEFEF", show="*", width=10)
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.ok_button = tk.Button(self.top, text="Ok", command=self.ok, bg="#2196F3", fg="white")
        self.ok_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        self.quit_button = tk.Button(self.top, text="Quit", command=self.cancel, bg="#F44336", fg="white")
        self.quit_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.top.bind("<Return>", self.ok)

    def ok(self, event=None):
        global nms
        if self.pass_entry.get() == "123Aa@":
            try:
                nms = int(self.nms_entry.get())
            except:
                messagebox.askokcancel("error", f"vui lòng nhập dạng số", icon=messagebox.ERROR)

        else:
            messagebox.askokcancel("error", f"sai mật khẩu", icon=messagebox.ERROR)
        self.top.destroy()
        nms_entry.config(text=f"{nms}")
        return nms

    def cancel(self, event=None):
        self.top.destroy()


def dialog():
    valor = StringVar()
    d = MyDialog(root, valor, "admin")
    root.wait_window(d.top)


def read_txt(file_name):
    with open(file=file_name, mode="r") as f:
        obj = f.readlines()

    return obj


def write_txt(file_name, text):
    with open(file=file_name, mode="w", encoding="utf8") as f:
        f.writelines(text)

    return 1


def check_max(a, sn):
    check = False
    try:
        max_num = int(nms)
        if a > int(nms):
            check = messagebox.askokcancel(title="waning",
                                           message=f"số bản ghi '{sn}.txt' là {a} đã vượt quá {max_num} tăng giá trị số bản ghi để tiếp tục",
                                           icon=messagebox.WARNING)

            dict_sn_save[sn] -= 1
        else:
            check = True

    except:
        messagebox.askokcancel("error", f"vui lòng nhập dạng số", icon=messagebox.ERROR)
        dict_sn_save[sn] -= 1
    return check


def check_value(sn: str) -> int:
    global dict_sn_save
    if dict_sn_save.get(sn) is not None:
        dict_sn_save[sn] += 1
    else:
        dict_sn_save[sn] = 1
    return dict_sn_save[sn]


def submit_form(event=None):
    global nms
    directory = "exportTxt"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        path = read_txt("path_save.txt")[0]
        if path:
            directory = path
    except:
        pass
    selected_model = model_var.get()
    sn = sn_entry.get()
    if len(sn) == 13:
        obj = read_txt(os.path.join("models", selected_model + ".txt"))
        obj = ["SN=" + sn + "\n"] + obj
        a = check_value(sn)
        print(a)
        check = check_max(a, sn)
        if check:
            write_txt(os.path.join(directory, sn + ".txt"), obj)
        sn_entry.delete(0, tk.END)
    else:
        sn_entry.delete(0, tk.END)


def select_directory():
    directory = filedialog.askdirectory()
    write_txt("path_save.txt", directory)
    return directory


def quit_app():
    # Hàm này sẽ được gọi khi nhấn nút Quit
    root.quit()


def get_options(dir_options):
    options = []
    for model in os.listdir(dir_options):
        if model and model[-3:] == "txt":
            options.append(model[:-4])
    return options


root = tk.Tk()
# root.iconbitmap("@icon/beer.ico")
root.title("ビール", )
root.configure(bg="#98F2DA")
frame = tk.Frame(root, bg="#FFFB8C")
frame.pack(pady=15, padx=15)

model_label = tk.Label(frame, text="MODELS  ", bg="#FFFB8C")
model_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
model_options = get_options("models")
model_var = tk.StringVar()
model_var.set(model_options[0])

model_dropdown = tk.OptionMenu(frame, model_var, *model_options)
model_dropdown.config(bg="#EFEFEF", width=24)
model_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W, columnspan=100)

sn_label = tk.Label(frame, text="SN  ", bg="#FFFB8C", bd=10)
sn_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

sn_entry = tk.Entry(frame, bg="#EFEFEF", width=30)
sn_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

nms_label = tk.Label(frame, text="Bản ghi tối đa ", bg="#FFFB8C", bd=10)
nms_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

nms_entry = tk.Label(frame, bg="#FFFB8C", width=25, bd=10, anchor=CENTER)
nms_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.NW)
nms_entry.config(text=f"{nms}")

button_frame = tk.Frame(frame, bg="#FFFB8C")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

url_button = tk.Button(button_frame, text="Đường dẫn", command=select_directory, bg="#2196F3", fg="white")
url_button.pack(side=tk.LEFT, padx=12)

adm_button = tk.Button(button_frame, text="Số bản ghi", command=dialog, bg="#2196F3", fg="white")
adm_button.pack(side=tk.LEFT, padx=12)

quit_button = tk.Button(button_frame, text="Quit", command=quit_app, bg="#F44336", fg="white")
quit_button.pack(side=tk.LEFT, padx=15)

root.bind("<Return>", submit_form)  # Đăng ký sự kiện nhấn Enter từ bàn phím để lưu form
while len(sn_entry.get()) == 2:
    submit_form()
root.mainloop()
