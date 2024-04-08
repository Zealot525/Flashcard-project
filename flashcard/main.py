from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Calibri"
ENGLISH_FONT = 20
LANGUAGE_FONT = 40
WORD_SIZE = 50
BOLD = "bold"
ITALIC = "italic"
current_card = {}

# #-------------------reading the word list in different files-------------------#
try:
    data = pandas.read_csv("data/list_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/n2.csv")
    data_dict = data.to_dict(orient="records")
    print(data_dict)
else:
    data_dict = data.to_dict(orient="records")


# #-------------------Creating new cards-------------------#
def create_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(canvas_bg, image=front_card)
    canvas.itemconfig(canvas_title, text="Japanese", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["Kanji"], fill="black", font=(FONT, WORD_SIZE,BOLD))
    canvas.itemconfig(canvas_reading, text=current_card["Kana"], fill="black")
    window.after(3000, func=flip_card)
    flip_timer = window.after(3000, func=flip_card)
        
        
# #-------------------Flipping cards to English-------------------#
def  flip_card():
        canvas.itemconfig(canvas_bg, image=back_card)
        canvas.itemconfig(canvas_title, text= "English", fill="white")
        canvas.itemconfig(canvas_word, text=current_card["English"], fill="white", font=(FONT, ENGLISH_FONT,BOLD))
        canvas.itemconfig(canvas_reading, text="")
        
# #-------------------Removing words from list & creating a new list of unlearned words-------------------#
def remove():
    data_dict.remove(current_card)
    dataframe = pandas.DataFrame(data_dict)
    dataframe.to_csv("data/list_to_learn.csv", index=False)
    create_card()
    

# #-------------------UI SETUP-------------------#
window = Tk()
window.title("JLPT N2 Flashcards")
window.config(padx=50, pady= 50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")

canvas = Canvas(width=800,height=526)
canvas.config(bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
canvas_bg = canvas.create_image(400,263, image=front_card)
canvas_title = canvas.create_text(400,150, text="Title", font=(FONT, LANGUAGE_FONT, ITALIC))
canvas_word = canvas.create_text(400,263,text="Word", font=(FONT, WORD_SIZE,BOLD))
canvas_reading = canvas.create_text(400,370, text="KANA", font=(FONT,WORD_SIZE,BOLD))
canvas.grid(column=0, row=0, columnspan=2)

wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=create_card)
wrong_button.grid(column=0, row=1)

right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=remove)
right_button.grid(column=1, row=1)

create_card()

window.mainloop()