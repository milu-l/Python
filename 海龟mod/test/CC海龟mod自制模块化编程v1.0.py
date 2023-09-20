import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def create_lua_file(folder_path):
    # 找到文件夹中的所有.lua文件
    lua_files = [file for file in os.listdir(folder_path) if file.endswith(".lua")]

    # 获取最大的数字命名
    max_number = 0
    for lua_file in lua_files:
        try:
            # 尝试将文件名解析为整数
            file_number = int(lua_file.split('.')[0])
            if file_number > max_number:
                max_number = file_number
        except ValueError:
            continue

    # 下一个数字命名
    next_number = max_number + 1

    # 创建.lua文件
    lua_file_path = os.path.join(folder_path, f"{next_number}.lua")

    # 创建.lua文件
    with open(lua_file_path, 'w') as file:
        # 在文件中写入内容（此处为空）
        pass

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        create_lua_file(folder_path)
        result_label.config(text=f"已在文件夹 {folder_path} 中创建.lua文件")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("选择的文件", f"您选择了文件: {file_path}")
        # 将选定文件的路径保存到全局变量
        global selected_file
        selected_file = file_path

def append_to_file(content, button_name):
    global selected_file
    if selected_file:
        with open(selected_file, 'a') as file:
            file.write(content + '\n')  # 追加内容，并添加换行符
        result_label.config(text=f"按钮'{button_name}'添加了内容: {content}")
        update_file_content_text(selected_file)  # 更新文件内容文本框

def delete_previous_line():
    global selected_file
    if selected_file:
        try:
            with open(selected_file, 'r') as file:
                lines = file.readlines()

            with open(selected_file, 'w') as file:
                text_widget.delete("sel.first - 1 lines", "sel.last - 1 lines")  # 删除选中的上一行
                for line in lines:
                    if line.strip() != text_widget.get(1.0, "end-1c").strip():  # 更新文件内容，跳过删除的行
                        file.write(line)

            result_label.config(text="已删除上一行内容")
            update_file_content_text(selected_file)  # 更新文件内容文本框
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

def clear_file_content():
    global selected_file
    if selected_file:
        try:
            with open(selected_file, 'w') as file:
                file.truncate(0)  # 清空文件内容
            text_widget.config(state=tk.NORMAL)  # 启用文本框
            text_widget.delete(1.0, tk.END)  # 清空文本框
            text_widget.config(state=tk.DISABLED)  # 禁用文本框，使其只读
            result_label.config(text="已清空文件内容")
        except Exception as e:
            messagebox.showerror("错误", f"无法清空文件内容: {str(e)}")

def update_file_content_text(file_path):
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            text_widget.config(state=tk.NORMAL)  # 启用文本框
            text_widget.delete(1.0, tk.END)  # 清空文本框
            text_widget.insert(1.0, file_content)  # 插入文件内容
            text_widget.config(state=tk.DISABLED)  # 禁用文本框，使其只读
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件内容: {str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("CC海龟mod自制模块化编程v1.0")

# 修改Tkinter窗口的图标
root.iconbitmap("./favicon.ico")  # 请替换成您的ICO图标文件路径

# 创建选择文件夹按钮
select_folder_button = tk.Button(root, text="选择文件夹并且创建文件.lua", command=select_folder)
select_folder_button.grid(row=0, column=0, padx=10, pady=20)

# 创建选择文件按钮
select_file_button = tk.Button(root, text="选择lua文件", command=select_file)
select_file_button.grid(row=1, column=0, padx=10, pady=10)

# 创建添加内容的按钮和标签
button_contents = [
    ("死循环", "while (true) do"),
    ("尝试将向前移动", "    turtle.forward()"),
    ("尝试将向后移动", "    turtle.back()"),
    ("尝试将向上移动", "    turtle.up()"),
    ("尝试将向下移动", "    turtle.down()"),
    ("向左转", "    turtle.turnLeft()"),
    ("向右转", "    turtle.turnRight()"),
    ("打破前面的障碍", "    turtle.dig()"),
    ("打破上面的块。", "    turtle.digUp() "),
    ("打破下方方块", "  turtle.digDown()"),
    ("加油", "turtle.refuel()"),
    ("在面前的攻击。", "turtle.attack()"),
    ("攻击上方。", "turtle.attackUp"),
    ("下的攻击。", "turtle.attackDown"),
    ("空", ""),
    ("空", ""),
    ("空", ""),
    ("空", ""),
    ("空", ""),
    ("空", "")
]

# 创建两列按钮
column1_buttons = []
column2_buttons = []

button_width = 20  # 按钮宽度
button_height = 2  # 按钮高度

for i, (button_name, content) in enumerate(button_contents):
    if i < 10:
        buttons = column1_buttons
        column = 0
    else:
        buttons = column2_buttons
        column = 1

    write_button = tk.Button(root, text=button_name, command=lambda c=content, b=button_name: append_to_file(c, b),
                             width=button_width, height=button_height)
    write_button.grid(row=i % 10 + 2, column=column, padx=10, pady=5, sticky='w')
    buttons.append(write_button)

# 创建结果显示标签
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=0, column=2, rowspan=12, padx=10, pady=20, sticky='n')

# 创建文本框（用于显示文件内容）
text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.grid(row=0, column=3, rowspan=12, padx=10, pady=10, sticky='nsew')
text_widget.config(state=tk.DISABLED)  # 设置文本框为只读

# 创建滚动条
scrollbar = tk.Scrollbar(root, command=text_widget.yview)
scrollbar.grid(row=0, column=4, rowspan=12, sticky='ns')
text_widget.config(yscrollcommand=scrollbar.set)

# 用于保存选定文件的全局变量
selected_file = None

# 创建删除文件内容中上一行的按钮
delete_previous_line_button = tk.Button(root, text="删除上一行", command=delete_previous_line)
delete_previous_line_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# 创建清空文件内容的按钮
clear_file_content_button = tk.Button(root, text="清空文件内容", command=clear_file_content)
clear_file_content_button.grid(row=12, column=2, columnspan=2, padx=10, pady=10)

# 启动主循环
root.mainloop()
