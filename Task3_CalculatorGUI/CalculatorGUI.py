import tkinter as tk

expression = ""


def press(value):
    global expression
    expression += str(value)
    display_var.set(expression)


def clear():
    global expression
    expression = ""
    display_var.set("")


def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)


def calculate():
    global expression
    if not expression:
        return
    try:
        result = eval(expression)
        display_var.set(result)
        expression = str(result)
    except ZeroDivisionError:
        display_var.set("can't divide by zero")
        expression = ""
    except Exception:
        display_var.set("invalid expression")
        expression = ""


root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)

display_var = tk.StringVar()
display = tk.Entry(
    root, textvariable=display_var, font=("Consolas", 20),
    justify="right", bd=8, relief="flat", bg="#eee"
)
display.grid(row=0, column=0, columnspan=4, ipady=15, sticky="ew")

buttons = [
    ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
    ("0", 5, 0), (".", 5, 1), ("<-", 5, 2), ("=", 5, 3),
]

for (text, row, col) in buttons:
    if text == "C":
        cmd = clear
    elif text == "<-":
        cmd = backspace
    elif text == "=":
        cmd = calculate
    else:
        cmd = lambda t=text: press(t)

    tk.Button(
        root, text=text, font=("Segoe UI", 14), command=cmd,
        width=4, height=2
    ).grid(row=row, column=col, sticky="nsew")

root.mainloop()
