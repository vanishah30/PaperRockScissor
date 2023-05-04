import sys
from random import randint
from tkinter import simpledialog, PhotoImage, Frame
from network import connect, send, close
from tkinter import *
from tk_sleep import tk_sleep


# create object

window = Tk()

window.geometry("500x500")

game_exit = False


def closing():
    close()
    window.destroy()
    game_exit = True


window.protocol("WM_DELETE_WINDOW", closing)


# title
window.title("Paper Rock Scissor Game")

game_state = {
    'me': None,
    'opponent': None,
    # "my_score": 0,
    # "opponent_score": 0,
    'my_selection': None,
    'opponent_selection': None,
}

verify_result = [
    ['Rock', 'Paper', 'opponent'],
    ['Paper', 'Rock', 'me'],
    ['Scissor', 'Rock', 'opponent'],
    ['Rock', 'Scissor', 'me'],
    ['Paper', 'Scissor', 'opponent'],
    ['Scissor', 'Paper', 'me'],
    
]


def result_evaluate():
    if game_state["my_selection"] and game_state["opponent_selection"]:
        my_sel_label.config(text= game_state["my_selection"] + "     ")
        Opponent_sel_label.config(text = game_state["opponent_selection"])
    if game_state["my_selection"] == game_state["opponent_selection"]:
        status_label.config(text= "Match Drawn")
    else:
        for x in verify_result:
            if x[0] == game_state["my_selection"] and x[1] == game_state["opponent_selection"]:
                status_label.config(text = game_state[x[2]] + " Won")


def reset_game():
    rock_btn["state"] = "active"
    paper_btn["state"] = "active"
    scissor_btn["state"] = "active"
    my_sel_label.config(text = "player     ")
    Opponent_sel_label.config(text = "opponent")
    status_label.config(text = "")
    game_state['my_selection'] = None
    game_state['opponent_selection'] = None
    status_label.config(text = game_state['opponent'] + " connected")


# disable the Button
def btn_disable():
    rock_btn["state"] = "disable"
    paper_btn["state"] = "disable"
    scissor_btn["state"] = "disable"
    


# if player select rock

def isrock():
    game_state["my_selection"] = "Rock"
    send("Rock")
    result_evaluate()
    btn_disable()

# if player select paper

def ispaper():
    game_state["my_selection"] = "Paper"
    send("Paper")
    result_evaluate()
    btn_disable()


def isscissor():
    game_state["my_selection"] = "Scissor"
    send("Scissor")
    result_evaluate()
    btn_disable()


# Add Labels, Frames and Button
Label(window, text="Paper Rock Scissor", font="calibri 20 bold", fg="blue").pack(pady=20)

frame = Frame(window)
frame.pack()


player_name_label = Label(
    window,
    text="",
    font="calibri 20 bold",
    bg="white",
    width=15,
    borderwidth=2,
    relief="solid",
)
player_name_label.pack(pady=20)


my_sel_label = Label(frame, text="Player  ", font=10)

vs_label = Label(frame, text="VS ", font="calibri 12 bold")

Opponent_sel_label = Label(frame, text="Opponent  ", font=10)

my_sel_label.pack(side=LEFT)
vs_label.pack(side=LEFT)
Opponent_sel_label.pack()

status_label = Label(
    window,
    text="",
    font="calibri 20 bold",
    bg="white",
    width=15,
    borderwidth=2,
    relief="solid",
)
status_label.pack(pady=20)

frame1 = Frame(window)
frame1.pack()

rock_img = PhotoImage(file = "C://Users//gasha12//Hello_python//PaperRockScissor//Images//rock.png")
paper_img = PhotoImage(file = "C://Users//gasha12//Hello_python//PaperRockScissor//Images//paper.png")
scissor_img = PhotoImage(file = "C://Users//gasha12//Hello_python//PaperRockScissor//Images//scissor.png")


rock_btn = Button(frame1, image=rock_img, command=isrock)

paper_btn = Button(frame1, image=paper_img, command=ispaper)

scissor_btn = Button(frame1, image=scissor_img, command=isscissor)

#rock_btn = Button(frame1, text="Rock",font=10,width=7, command=isrock)

#paper_btn = Button(frame1, text="Paper",font=10,width=7, command=ispaper)

#scissor_btn = Button(frame1, text="Scissor",font=10,width=7, command=isscissor)

rock_btn.pack(side=LEFT, padx= 10)
paper_btn.pack(side=LEFT, padx=10)
scissor_btn.pack(padx= 10)


Button(
    window, text="Reset Game", font=10, fg="red", bg="yellow", command=reset_game
).pack(pady=20)


def get_opponent_and_decide_game_runner(user, message):
    # who is the server (= the creator of the channel)
    if "created the channel" in message:
        name = message.split("'")[1]
        # game_state["is_server"] = name == game_state['me']
    # who is the opponent (= the one that joined that is not me)
    if "joined channel" in message:
        name = message.split(" ")[1]
        if name != game_state["me"]:
            game_state["opponent"] = name


def message_handler(timestamp, user, message):
    if user == "system":
        get_opponent_and_decide_game_runner(user, message)

    if user == game_state["opponent"] and type(message) is str:
        game_state["opponent_selection"] = message
        result_evaluate()


def start():
    status_label.config(text="Not connected")


# connect to newtwork

game_state["me"] = simpledialog.askstring("Input", "Your name", parent=window)

channel = simpledialog.askstring("Input", "Channel", parent=window)
connect(channel, game_state["me"], message_handler)
player_name_label.config(text=game_state["me"])

# wait for opponent

while game_state["opponent"] == None and game_exit == False:
    tk_sleep(window, 1 / 10)
status_label.config(text = game_state["opponent"] + " connected")


start()
window.mainloop()
