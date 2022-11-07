import tkinter as tk
import tkinter.font as font
import random

# flake8: noqa

# creating window
window = tk.Tk()
window.resizable(False, False)
window.title("Tic-Tac-Toe")

# default font
myFont = font.Font(family="Courier", size=20, weight="bold")
# font for X and O in grid
gridFont = font.Font(family="Courier", size=36, weight="bold")

# label to display updates like turn and activated bots
label = tk.Label(
    window, text="Player X Turn", font=myFont, bg="LightSteelBlue4", fg="white"
)
label.grid(row=0, column=0)

# frame for holding squares for grid
play_area = tk.Frame(window, width=300, height=30, bg="honeydew2")
play_area.grid(row=1, column=0)

# class to hold variables
class State:
    current_char = "X"
    X_points = []
    O_points = []
    game_over = False
    buttons = {}
    square = None
    robot_active = False
    bot_turn = False
    turn_count = 0


# function to change label text cleaner
def update_label(text):
    label.configure(text=text)


# resets board and then sets O as starting character
def start_O():
    reset_board()
    State.current_char = "O"
    update_label(f"Player {State.current_char} Turn")


def bot_selector():
    if State.game_over is False:
        if State.robot_active == "Easy":
            easy_robot()
        elif State.robot_active == "Hard":
            hard_robot()


def easy_robot():
    while State.bot_turn is True:
        # randomly generates a x,y point
        x = random.randint(1, 3)
        y = random.randint(1, 3)
        # retrieves button from dict using the generated point
        button = State.buttons[x, y]
        print(x, y, button.value)
        # checks if the button has been clicked before
        if button.value is None:
            # if empty square bot fills square and ends turn
            button.set_square()


class TwoInLine:
    def __init__(self, p1, p2, p3):
        # takes point from inputted rows
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def check(self, for_char):
        p1_satisfied = False
        p2_satisfied = False
        p3_satisfied = False
        # if X has all 3 points in the row
        if for_char == "X":
            for coord in State.X_points:
                if coord.p == self.p1:
                    p1_satisfied = True
                elif coord.p == self.p2:
                    p2_satisfied = True
                elif coord.p == self.p3:
                    p3_satisfied = True
        # checks if O has all 3 points in the row
        elif for_char == "O":
            for coord in State.O_points:
                if coord.p == self.p1:
                    p1_satisfied = True
                elif coord.p == self.p2:
                    p2_satisfied = True
                elif coord.p == self.p3:
                    p3_satisfied = True
        # returns results
        return [p1_satisfied, p2_satisfied, p3_satisfied]


two_in_line = [
    TwoInLine((1, 1), (1, 2), (1, 3)),
    TwoInLine((2, 1), (2, 2), (2, 3)),
    TwoInLine((3, 1), (3, 2), (3, 3)),
    TwoInLine((1, 1), (2, 1), (3, 1)),
    TwoInLine((1, 2), (2, 2), (3, 2)),
    TwoInLine((1, 3), (2, 3), (3, 3)),
    TwoInLine((1, 1), (2, 2), (3, 3)),
    TwoInLine((3, 1), (2, 2), (1, 3)),
    ]


def hard_robot():
    if State.turn_count == 0:
        button = State.buttons[2,2]
        if button.value is None:
            button.set_square()
        else:
            button = State.buttons[1, 1]
            button.set_square()
        State.turn_count += 1
    elif State.turn_count == 1:
        for line in two_in_line:
            line_X = line.check("X")
            line_Y = line.check("X")
        State.turn_count += 1
        
        

    #while State.bot_turn is True:
    


class Square:
    # using dunder init to make buttons
    def __init__(self, x, y):
        self.p = (x, y)
        self.value = None
        self.button = tk.Button(
            play_area,
            text=" ",
            width=5,
            height=2,
            command=self.btn_op,
            bg="gainsboro",
            font=gridFont,
            pady=10,
        )

    # operation that runs every time that a button is clicked
    def btn_op(self):
        # checks if game is over
        if State.game_over is not True:
            self.set_square()
            bot_selector()

    def set_square(self):
        # if button has been clicked before do nothing
        if self.value is None:
            # if not clicked before set value to X or O and update label
            self.value = State.current_char
            self.button.configure(text=State.current_char, bg="ivory4", fg="black")
            # if it's X's turn make it O's and add clicked square to list
            # if the bot is active it is now it's turn
            if State.current_char == "X":
                State.current_char = "O"
                State.X_points.append(self)
                State.bot_turn = True
            else:
                State.current_char = "X"
                State.O_points.append(self)
                State.bot_turn = False
            # updates the label to be the current players turn
            update_label(f"Player {State.current_char} Turn")
        check_win()

    def reset(self):
        # individual button clears it's label and value
        self.button.configure(text="", bg="gainsboro")
        self.value = None


# class to check if game is won
class WinningStates:
    def __init__(self, p1, p2, p3):
        # takes point from inputted rows
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def check(self, for_char):
        p1_satisfied = False
        p2_satisfied = False
        p3_satisfied = False
        # if X has all 3 points in the row
        if for_char == "X":
            for coord in State.X_points:
                if coord.p == self.p1:
                    p1_satisfied = True
                elif coord.p == self.p2:
                    p2_satisfied = True
                elif coord.p == self.p3:
                    p3_satisfied = True
        # checks if O has all 3 points in the row
        elif for_char == "O":
            for coord in State.O_points:
                if coord.p == self.p1:
                    p1_satisfied = True
                elif coord.p == self.p2:
                    p2_satisfied = True
                elif coord.p == self.p3:
                    p3_satisfied = True
        # returns results
        return all([p1_satisfied, p2_satisfied, p3_satisfied])


# generates squares placed in grid
# then sticky stretches them to fit perfectly
for x in range(1, 4):
    for y in range(1, 4):
        State.buttons[(x, y)] = State.square = Square(x, y)
        State.square.button.grid(row=x, column=y, sticky="nsew")

# list containing all possible winning states
# including diagonal, rows, and columns
winning_states = [
    WinningStates((1, 1), (1, 2), (1, 3)),
    WinningStates((2, 1), (2, 2), (2, 3)),
    WinningStates((3, 1), (3, 2), (3, 3)),
    WinningStates((1, 1), (2, 1), (3, 1)),
    WinningStates((1, 2), (2, 2), (3, 2)),
    WinningStates((1, 3), (2, 3), (3, 3)),
    WinningStates((1, 1), (2, 2), (3, 3)),
    WinningStates((3, 1), (2, 2), (1, 3)),
]

# if player has won color the winning points
def show_winning_line(state):
    for x, y in [(state.p1), (state.p2), (state.p3)]:
        # uses x,y to get points from dictionary
        square = State.buttons[(x, y)]
        # colors buttons retrieved from dictionary
        square.button.configure(bg="coral")


# whenever a button is clicked run function
def check_win():
    # checks through the winning_states list
    for state in winning_states:
        # checks each row for character X
        if state.check("X"):
            # if X has winning state update label, winning line and end game
            update_label("Player X Wins")
            State.game_over = True
            show_winning_line(state)
            return
        if state.check("O"):
            # if O has winning state update label, winning line and end game
            update_label("Player O Wins")
            State.game_over = True
            show_winning_line(state)
            return
    # checks if all squares filled
    if len(State.X_points) + len(State.O_points) == 9:
        # if grid filled end game and update label
        update_label("Draw")
        State.game_over = True


# each button resets itself clearing its value and text
def reset_board():
    for State.square in State.buttons.values():
        State.square.reset()
    # update label and reset variables
    State.current_char = "X"
    State.X_points = []
    State.O_points = []
    State.game_over = False
    State.turn_count = 0
    update_label(f"Player {State.current_char} Turn")


# activates and deactivates easy bot
def start_easy():
    reset_board()
    if State.robot_active != "Easy":
        State.robot_active = "Easy"
        update_label("Easy Bot Active")
    else:
        # if easy bot active then deactivate
        State.robot_active = False
        update_label("Easy Bot Disabled")


def start_hard():
    reset_board()
    if State.robot_active != "Hard":
        State.robot_active = "Hard"
        update_label("Hard Bot Active")
    else:
        # if easy bot active then deactivate
        State.robot_active = False
        update_label("Hard Bot Disabled")


# creating button to reset grid
reset_btn = tk.Button(window, text="Reset", font=myFont, command=reset_board)
reset_btn.grid(row=2, column=0)

# creating menubar
menubar = tk.Menu(window)
game_menu = tk.Menu(menubar, tearoff=0)
game_menu.add_command(label="Reset Game", command=reset_board)
game_menu.add_command(label="Start with O", command=start_O)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=window.destroy)
AI_menu = tk.Menu(menubar, tearoff=0)
AI_menu.add_command(label="Activate Easy Bot", command=start_easy)
AI_menu.add_command(label="Activate Hard Bot", command=start_hard)
menubar.add_cascade(label="Game", menu=game_menu)
menubar.add_cascade(label="AI", menu=AI_menu)

window.config(menu=menubar)

window.mainloop()
