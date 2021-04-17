import json,time
from difflib import get_close_matches
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar,Frame
import brain


import os
os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))
path_intents = "data/intents.json"

class Chatbot:
    def __init__(self, window):
        window.title('Batman Assitant')
        window.geometry('600x600')
        window.resizable(0,0)

        self.message_session = Text(window, bd=3, relief="flat", font=("Comic Sans MS", 19, "bold"), undo=True, wrap="word")
        self.message_session.config(width=45, height=15,bg="#000000", fg="green", state='disabled')
        self.overscroll = Scrollbar(window, command=self.message_session.yview)
        self.overscroll.config(width=20)
        self.message_session["yscrollcommand"] = self.overscroll.set
        self.message_position = 1.5
        self.send_button = Button(window, text='Send', fg='green', bg='black',width=5,font=('Times', 17, "bold"), relief ='flat', command = self.reply_to_you)
        self.Message_Entry = Entry(window, width=35 ,font=("Times", 17, "bold"), bg='grey', fg='black')
        self.Message_Entry.bind('<Return>', self.reply_to_you)
        self.message_session.place(x=20, y=20,height=460, width=560)
        self.overscroll.place(x=557, y=423)
        self.send_button.place(x=500, y=480, height=100 , width=80)
        self.Message_Entry.place(x=20, y=480, height=100, width=470)
        self.Brain = json.load(open(path_intents))

    def add_chat(self, message,color="green"):
        print('---------------------------')
        
        self.message_position+=1.5
        #print(self.message_position)
        self.Message_Entry.delete(0, 'end')
        self.message_session.config(state='normal', fg=color)
        self.message_session.insert(self.message_position, message)
        self.message_session.see('end')
        self.message_session.config(state='disabled')


    
    def reply_to_you(self, event=None):
        message = self.Message_Entry.get().lower()
        
        res = brain.main(message)
        
        message = 'you: '+ message+'\n'
        
        self.add_chat(message,color="blue")
        res = 'goku: '+res+'\n\n'
        self.add_chat(res, color="green")

def main():
    root = Tk()
    Chatbot(root)
    root.mainloop()


if __name__ == "__main__":
    main()
