from tkinter import *
import random
import statistics
TIMER_MS = 0
TIMER_SEC = 0
TIMER = None
WORD: str = ""


def stop_game():
    global TIMER_MS, TIMER_SEC
    TIMER_MS = 0
    TIMER_SEC = 0
    window.after_cancel(TIMER)
    start_button.config(text="go", command=start_game)
    try:
        with open("wordxdata.txt", "r") as f:
            data = f.readlines()
    except FileNotFoundError as e:
        raise e
    else:
        del data[0]
        typed_list = [text.strip("\n").split("|")[0] for text in data]
        word_list = [text.strip("\n").split("|")[2] for text in data]
        time_list = [text.strip("\n").split("|")[1] for text in data]
        total_word = []
        for i in range(len(data)):
            if typed_list[i] == word_list[i]:
                total_word.append(data[i].strip("\n").split("|")[2])
        time_mean = statistics.mean([float(string.replace(":", ".")) for string in time_list])
        word_per_minute = (len(total_word) / time_mean) * 60
        word_label.config(text=f"You type: {round(word_per_minute, 2)} wpm")


def game_logic(event=None):
    global TIMER_MS, TIMER_SEC
    type_word = type_entry.get()
    type_entry.delete(first=0, last=END)
    with open("wordxdata.txt", "a+") as f:
        f.write(f"\n{type_word}|{TIMER_SEC}:{TIMER_MS}|{WORD}")
    get_word()
    TIMER_MS = 0
    TIMER_SEC = 0


def start_game():
    start_button.config(text="Stop", command=stop_game)
    stop_watch()
    get_word()
    with open("wordxdata.txt", "w") as f:
        pass


def stop_watch():
    global TIMER_MS, TIMER_SEC, TIMER
    TIMER_MS += 1
    if TIMER_MS == 100:
        TIMER_SEC += 1
        TIMER_MS = 0
    if 100 > TIMER_MS >= 10:
        time_label.config(text=f"{TIMER_SEC}:0{TIMER_MS}")
    elif 10 > TIMER_MS:
        time_label.config(text=f"{TIMER_SEC}:00{TIMER_MS}")
    TIMER = window.after(10, stop_watch)


def get_word():
    global WORD
    with open("words_alpha.txt") as f:
        words = f.read().split()

    WORD = random.choice(words)
    word_label.config(text=WORD)


window = Tk()
window.title("Typing Speed Test")
window.config(bg="black")
window.geometry("1000x300")
window.bind("<Return>", game_logic)

word_label = Label(
    text="Click 'Go' to start", bg="black", fg="white",
    font=("Times new roman", 32, "bold"),
    pady=25,
    padx=25,
    anchor=CENTER,
    width=25
)
word_label.grid(row=0, column=1)

time_label = Label(
    text="00:000",
    bg="Black",
    fg="white",
    font=("Times new roman", 32, "bold"),
    padx=25,
    pady=25,
    anchor=CENTER
)
time_label.grid(row=2, column=0)

type_entry = Entry(width=25, justify=CENTER)
type_entry.focus()
type_entry.grid(row=1, column=1, pady=(50, 0))

start_button = Button(text="Go", pady=3, padx=15, anchor=CENTER, command=start_game)
start_button.grid(row=2, column=2)


window.mainloop()
