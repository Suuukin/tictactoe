import tkinter as tk
import tkinter.font as font
import random

MARKER_X = "X"
MARKER_O = "O"
MARKER_EMPTY = " "


class State:
    """Holds global state for game."""

    # marker for the next player
    current_char = MARKER_X

    # stores markers for each point on the board
    board = {}  # {point: marker}

    # True if the game is over (win, loss, draw)
    game_over = False

    # Tkinter buttons for each square of board
    buttons = {}  # {point: Square}

    # text label at top of window
    label = None

    # set to "Easy", "Medium" or "Hard" if bot is active
    robot_active = False

    # True if it is bot's turn to play
    bot_turn = False

    # number of turns played so far
    turn_count = 0


# List containing points of all possible winning lines (rows, columns,
# diagonals).
LINES = [
    [(1, 1), (1, 2), (1, 3)],
    [(2, 1), (2, 2), (2, 3)],
    [(3, 1), (3, 2), (3, 3)],
    [(1, 1), (2, 1), (3, 1)],
    [(1, 2), (2, 2), (3, 2)],
    [(1, 3), (2, 3), (3, 3)],
    [(1, 1), (2, 2), (3, 3)],
    [(3, 1), (2, 2), (1, 3)],
]

CORNERS = [(1, 1), (1, 3), (3, 1), (3, 3)]

SIDES = [(1, 2), (2, 1), (2, 3), (3, 2)]


def update_label(text):
    """update label text at top of window"""
    State.label.configure(text=text)


def start_O():
    """reset the board and then set O as starting character"""
    reset_board()
    State.current_char = "O"
    update_label(f"Player {State.current_char} Turn")


def bot_selector():
    """Check if bot needs to run and run selected bot type."""
    if not State.game_over and State.bot_turn:
        if State.robot_active == "Easy":
            easy_robot()
        elif State.robot_active == "Medium":
            medium_robot()
        elif State.robot_active == "Hard":
            hard_robot()


def easy_robot():
    while State.bot_turn:
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


def check_two_in_line(line, marker):
    """Check if two of same markers are in a line, return the empty point.
    If line doesn't meet these conditions, return None."""
    markers = []
    for p in line:
        markers.append(State.board[p])
    found = markers.count(MARKER_EMPTY) == 1 and markers.count(marker) == 2
    if found:
        for p in line:
            if State.board[p] == MARKER_EMPTY:
                return p
    return None


def medium_robot():
    if not State.bot_turn:
        return
    for marker in [MARKER_O, MARKER_X]:
        for line in LINES:
            square_coord = check_two_in_line(line, marker)
            if square_coord is not None:
                button = State.buttons[square_coord]
                button.set_square()
                State.turn_count += 1
                return
    easy_robot()


def check_free_line(line, marker):
    """Check if line has one marker and two empty squares, return list
    of empty points."""
    markers = []
    for p in line:
        markers.append(State.board[p])
    free = markers.count(MARKER_EMPTY) == 2 and markers.count(marker) == 1
    potential_points = []
    if free:
        for p in line:
            if p in CORNERS:
                if State.board[p] == MARKER_EMPTY:
                    potential_points.append(p)
    return potential_points


def hard_robot():
    if not State.bot_turn:
        return

    for marker in [MARKER_O, MARKER_X]:
        for line in LINES:
            square_coord = check_two_in_line(line, marker)
            if square_coord is not None:
                button = State.buttons[square_coord]
                button.set_square()
                State.turn_count += 1
                return

    if not State.bot_turn:
        return

    if State.turn_count == 0:
        State.turn_count += 1
        if State.board[(2, 2)] == MARKER_EMPTY:
            button = State.buttons[(2, 2)]
            button.set_square()
        else:
            corner = random.choice(CORNERS)
            button = State.buttons[corner]
            button.set_square()
        return

    if State.turn_count == 1:
        if (
            State.board[1, 1] is MARKER_X
            and State.board[3, 3] is MARKER_X
            or State.board[1, 3] is MARKER_X
            and State.board[3, 1] is MARKER_X
        ):
            print("placing side")
            side = random.choice(SIDES)
            button = State.buttons[side]
            button.set_square()
            State.turn_count += 1

        if State.board[1, 2] is MARKER_X and State.board[2, 1] is MARKER_X:
            button = State.buttons[1, 1]
            button.set_square()
            State.turn_count += 1

        if State.board[2, 3] is MARKER_X and State.board[3, 2] is MARKER_X:
            button = State.buttons[3, 3]
            button.set_square()
            State.turn_count += 1

    if State.bot_turn:
        potential_points = []
        for line in LINES:
            free = check_free_line(line, MARKER_O)
            potential_points.extend(free)
        if potential_points:
            point = random.choice(potential_points)
            button = State.buttons[point]
            button.set_square()

    easy_robot()


class Square:
    """A single square on the board, with button to press."""

    def __init__(self, play_area, x, y):
        self.p = (x, y)  # the point for this button
        self.value = None  # the marker at this square (X or O or empty)
        self.button = tk.Button(
            play_area,
            text=" ",
            width=5,
            height=2,
            command=self.btn_op,
            bg="gainsboro",
            font=GRID_FONT,
            pady=10,
        )

    # operation that runs every time that a button is clicked
    def btn_op(self):
        # checks if game is over
        if not State.game_over:
            self.set_square()
            bot_selector()

    def set_square(self):
        # if button has been clicked before do nothing
        if self.value is None:
            # if not clicked before set value to X or O and update label
            self.value = State.current_char
            self.button.configure(
                text=State.current_char, bg="ivory4", fg="black"
            )
            # if it's X's turn make it O's and add clicked square to list
            # if the bot is active it is now it's turn
            if State.current_char == "X":
                State.current_char = "O"
                State.board[self.p] = MARKER_X
                State.bot_turn = True
            else:
                State.current_char = "X"
                State.board[self.p] = MARKER_O
                State.bot_turn = False
            # updates the label to be the current players turn
            update_label(f"Player {State.current_char} Turn")
        check_win()

    def reset(self):
        # individual button clears it's label and value
        self.button.configure(text=" ", bg="gainsboro")
        self.value = None


def check_win_state(line):
    """check if game is won along 'line'"""
    markers = []
    # if X has all 3 points in the row
    for p in line:
        markers.append(State.board[p])
    if markers.count(MARKER_X) == 3:
        return MARKER_X
    if markers.count(MARKER_O) == 3:
        return MARKER_O
    return None


# if player has won color the winning points
def show_winning_line(line):
    for x, y in line:
        # uses x,y to get points from dictionary
        square = State.buttons[(x, y)]
        # colors buttons retrieved from dictionary
        square.button.configure(bg="coral")


# whenever a button is clicked run function
def check_win():
    for line in LINES:
        # checks each row for character X
        win_marker = check_win_state(line)
        if win_marker == MARKER_X:
            # if X has winning state update label, winning line and end game
            update_label("Player X Wins")
            State.game_over = True
            show_winning_line(line)
            return
        if win_marker == MARKER_O:
            # if O has winning state update label, winning line and end game
            update_label("Player O Wins")
            State.game_over = True
            show_winning_line(line)
            return
    # checks if all squares filled
    markers = set(State.board.values())
    if MARKER_EMPTY not in markers:
        # if grid filled end game and update label
        update_label("Draw")
        State.game_over = True


# each button resets itself clearing its value and text
def reset_board():
    for square in State.buttons.values():
        square.reset()
    # update label and reset variables
    State.current_char = "X"
    for p in State.board:
        State.board[p] = MARKER_EMPTY
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


def start_medium():
    reset_board()
    if State.robot_active != "Medium":
        State.robot_active = "Medium"
        update_label("Medium Bot Active")
    else:
        # if easy bot active then deactivate
        State.robot_active = False
        update_label("Medium  Bot Disabled")


def start_hard():
    reset_board()
    if State.robot_active != "Hard":
        State.robot_active = "Hard"
        update_label("Hard Bot Active")
    else:
        # if easy bot active then deactivate
        State.robot_active = False
        update_label("Hard Bot Disabled")


def main():
    global MY_FONT, GRID_FONT

    # creating window
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Tic-Tac-Toe")

    # default font
    MY_FONT = font.Font(family="Courier", size=20, weight="bold")

    # font for X and O in grid
    GRID_FONT = font.Font(family="Courier", size=36, weight="bold")

    # label to display updates like turn and activated bots
    State.label = tk.Label(
        window,
        text="Player X Turn",
        font=MY_FONT,
        bg="LightSteelBlue4",
        fg="white",
    )
    State.label.grid(row=0, column=0)

    # frame for holding squares for grid
    play_area = tk.Frame(window, width=300, height=30, bg="honeydew2")
    play_area.grid(row=1, column=0)

    # generates squares placed in grid
    # then sticky stretches them to fit perfectly
    for x in range(1, 4):
        for y in range(1, 4):
            State.buttons[(x, y)] = square = Square(play_area, x, y)
            square.button.grid(row=x, column=y, sticky="nsew")
            State.board[(x, y)] = MARKER_EMPTY  # all points are empty

    # creating button to reset grid
    reset_btn = tk.Button(
        window, text="Reset", font=MY_FONT, command=reset_board
    )
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
    AI_menu.add_command(label="Actiate Medium Bot", command=start_medium)
    AI_menu.add_command(label="Activate Hard Bot", command=start_hard)
    menubar.add_cascade(label="Game", menu=game_menu)
    menubar.add_cascade(label="AI", menu=AI_menu)

    window.config(menu=menubar)

    window.mainloop()


if __name__ == '__main__':
    main()
