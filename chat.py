import socket
import sys
from threading import Thread
from tkinter import *
from tkinter import messagebox

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "0.0.0.0"
port = 81
s.bind((ip, port))

num = 1
users = {"192.168.56.102": ["JOHN", "dark green"],
         "192.168.56.103": ["TOM", "DarkOrchid4"]}

# send and display the data on button click
def clicked():
    global num
    try:
        data = txtfld.get().rstrip()
        if data != '':
            for ip in users.keys():
                s.sendto(data.encode(), (ip, 81))
            Label(msgframe, text=f"▷ {data}", fg='SlateBlue4', font=10, bg='lavender').grid(
                row=num, column=1, sticky=E, padx=20)
            num += 1
        canvas.yview_moveto('1.0')
    except Exception as e:
        messagebox.showerror('Error', e)


# recieving data and display
def recieve():
    global num
    try:
        while True:
            data = s.recvfrom(1024)
            Label(msgframe, text=f"{users[data[1][0]][0]}:", fg=users[data[1][0]][1], bg='lavender').grid(
                row=num, column=0, sticky=W, padx=20)
            num += 1
            Label(msgframe, text=f"▷ {data[0].decode()}", fg=users[data[1][0]][1], font=10, bg='lavender').grid(
                row=num, column=0, sticky=W, padx=20)
            num += 1
            canvas.yview_moveto('1.0')
    except Exception as e:
        if s._closed:
            print("Program is terminated")
        else:
            print(e)


# thread to start recieving data
t = Thread(target=recieve)
t.daemon = True
t.start()

# scroller for canvas
def myfunction(event):
    canvas.configure(scrollregion = canvas.bbox("all"))

# setting width of msgframe equal to canvas width
def frameWidth(event):
    canvas_width = event.width
    canvas.itemconfig(canvas_frame, width = canvas_width)

# creating window
root = Tk()
root.title('ChAt (192.168.56.1) - Hello Eric!')
root.geometry("700x600+350+150")
uinput = StringVar()


# header frame
head = Frame(root, relief=RAISED, borderwidth=0, bg='bisque')
head.pack(fill=X, side=TOP)
Label(head, text="Group Chat", font=15, bg='bisque').pack(
    side='left', padx=10, pady=4)

# frame where message will print, in a scrollable canvas
myframe = Frame(root, relief=GROOVE, bd=1)
myframe.pack(fill=BOTH, expand=True, side=TOP)
canvas = Canvas(myframe, bg='lavender')
msgframe = Frame(canvas, relief=RAISED, borderwidth=0, bg='lavender')
msgframe.columnconfigure(1, weight=1)
msgframe.pack(fill=BOTH, expand=True, side=TOP, pady=20)
myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side="right", fill="y", expand=False)
canvas.pack(fill=BOTH, side="top", expand=True)
canvas_frame = canvas.create_window(0, 0, window=msgframe, anchor='nw')
msgframe.bind("<Configure>", myfunction)
canvas.bind('<Configure>', frameWidth)

# footer frame, taking input
frame = Frame(root, relief=RAISED, borderwidth=0, bg='bisque')
frame.pack(fill=X, side=BOTTOM)
btn = Button(frame, text="SEND", fg='SlateBlue4', width=10, font=4,
             activeforeground='white', activebackground='SlateBlue4', borderwidth=1, command=clicked)
btn.pack(side=RIGHT, expand=True, padx=10, pady=4)
txtfld = Entry(frame, textvariable=uinput, bd=1,
               width=150, font=10, fg='SlateBlue4')
txtfld.pack(side=BOTTOM, expand=True, padx=10, pady=4)

# looping the window
root.mainloop()

s.close()
sys.exit()
