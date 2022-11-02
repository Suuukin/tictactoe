import tkinter as tk
import tkinter.font as font

window = tk.Tk()
window.title("TicTacToe")

myFont = font.Font(family="Courier", size=20, weight="bold")

class State:
    turn_tracker = None


def make_btn(parent, label):
    return tk.Button(
        parent,
        padx=33,
        pady=20,
        text=None,
        font=myFont,
        command=lambda: btn_op(label),
    )


def update_label():
    start_button.configure(text="Restart")
    if State.turn_tracker == 1:
        label.configure(text="Player 1's turn!")
    elif State.turn_tracker == 2:
        label.configure(text="Player 2's turn!")


def win_check():
    return


def btn_op(label):
    if State.turn_tracker == 1:
        State.turn_tracker = 2
        buttons[label].configure(text='X')
    else:
        State.turn_tracker = 1
        buttons[label].configure(text='O')
    win_check()
    update_label()



def restart(label):
    State.turn_tracker = 1
    update_label()
    for button in buttons.items():
        button.configure(text=None)


label = tk.Label(window, text="Play TicTacToe", font=myFont)
label.grid(column=0, row=0, columnspan=4, sticky='nsew')

play_area = tk.Frame(window)
play_area.grid(column=0, row=1, columnspan=4, rowspan=4)

start_button = tk.Button(window, text="Start Game", command=restart)
start_button.grid(column=0, row=5, columnspan=4, sticky='nsew')


buttons = {}
for i in range(9):
    buttons[i] = b = make_btn(play_area, i)
    row, column = divmod(i, 3)
    # this makes the buttons pad themselves to fit the frame
    b.grid(row=row, column=column, sticky="nsew")


window.mainloop()
