from tkinter import * 
from tkinter import simpledialog
import math

# ---------------------------- CONSTANTS ------------------------------- #

CHECKMARK = "✔"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

root = Tk()
root.withdraw()

WORK_MIN = simpledialog.askinteger("Pomodoro Setup", "Enter work duration in minutes:", 
                                   initialvalue=25, minvalue=1, maxvalue=120)
if WORK_MIN is None:    
	WORK_MIN = 25

root.destroy()

SHORT_BREAK_MIN = WORK_MIN / 5
LONG_BREAK_MIN = SHORT_BREAK_MIN * 4
PATH_IMAGE = "tomato.png"
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="TIMER")
    check_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = int(SHORT_BREAK_MIN * 60)
    long_break_sec = int(LONG_BREAK_MIN * 60)
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="BREAK", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="BREAK", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="WORK", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
         count_sec = "00"
    else:
        if count_sec < 10:
            count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_session = math.floor(reps/2)
        for n in range(work_session):
            marks += "✔"
        check_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title(f"Pomodoro - {WORK_MIN} min sessions")
window.config(padx=100,pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

try:
    tomato_img = PhotoImage(file=PATH_IMAGE)
    canvas.create_image(100, 110, image=tomato_img)
except:
    canvas.create_oval(50, 60, 150, 160, fill=RED, outline="darkred", width=3)
    canvas.create_oval(85, 50, 100, 65, fill=GREEN)
    canvas.create_oval(100, 50, 115, 65, fill=GREEN)

timer_text = canvas.create_text(100, 134, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1)

title_label = Label(text="TIMER", fg=GREEN, bg=YELLOW , font=(FONT_NAME, 40, "bold"))
title_label.grid(column=1, row=0)

start_button = Button(text="START", bg=YELLOW , font=(FONT_NAME, 13, "bold"), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="RESET", bg=YELLOW , font=(FONT_NAME, 13, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

check_label = Label(fg=GREEN, bg=YELLOW , font=(FONT_NAME, 14, "bold"))
check_label.grid(column=1, row=3)

window.mainloop()