# import random, json , pickle, numpy as np,os
# import nltk
# from nltk.stem import WordNetLemmatizer
# from tensorflow.keras.models import load_model
# os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))

# lemmatizer = WordNetLemmatizer()
# intents = json.loads(open('data/intents.json').read())

# words = pickle.load(open('words.pkl', 'rb'))
# classes = pickle.load(open('classes.pkl', 'rb'))
# model = load_model('chatbot.h5')


# def _clean_up_sentence(sentence):
#     sentence_words = nltk.word_tokenize(sentence)
#     sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
#     return sentence_words

# def _bag_of_words(sentence, words):
#     sentence_words = _clean_up_sentence(sentence)
#     bag = [0] * len(words)
#     for s in sentence_words:
#         for i, word in enumerate(words):
#             if word == s:
#                 bag[i] = 1
#     return np.array(bag)

# def _predict_class(sentence):
#     p = _bag_of_words(sentence, words)
#     res = model.predict(np.array([p]))[0]
#     ERROR_THRESHOLD = 0.1
#     results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

#     results.sort(key=lambda x: x[1], reverse=True)
#     return_list = []
#     for r in results:
#         return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
#     return return_list

# def _get_response(ints, intents_json):
#     try:
#         tag = ints[0]['intent']
#         list_of_intents = intents_json['intents']
#         for i in list_of_intents:
#             if i['tag']  == tag:
#                 result = random.choice(i['responses'])
#                 break
#     except IndexError:
#         result = "I don't understand!"
#     return result


# print("Chatbot is open\n")
# while True:
#     message = input("")
#     ints = _predict_class(message)
#     #print(ints)
#     res = _get_response(ints, intents)
#     print(res, ints[0]['probability'], "intent is ",ints[0]['intent'])
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

##########################################################################################


import random, json , pickle, numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os,time
import hand_app
import pyjokes

os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))
intents = json.loads(open('data/intents.json').read())
lemmatizer = WordNetLemmatizer()


words = pickle.load(open('models/words.pkl', 'rb'))
classes = pickle.load(open('models/classes.pkl', 'rb'))
model = load_model('models/chatbot.h5')
context = {}
tagDict = {"terminal":"gnome-terminal", "gedit":"gedit"}

def run_commands(response,tag):
    if "incognito" in response:
        os.system("google-chrome --incognito")
        return(response)
    elif "chrome" in response:
        os.system("google-chrome")
        return(response)
    elif "chrome" in response:
        os.system("google-chrome")
        return(response)
    elif "date" in tag:
        return(response + str(time.time()))
    elif "hand_app" in tag:
        hand_app.camera()
        return(response)
    elif tag in tagDict:
        os.system(tagDict[tag])
        return(response)
    elif "joke" in tag:
        return (pyjokes.get_joke())
    else:
        return(response)
        
    
    


def _clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def _bag_of_words(sentence, words):
    sentence_words = _clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def _predict_class(sentence):
    p = _bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.3
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    if len(results)==0:
        results="Dont know what you are talking about"
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list





def _get_response(message, intents, userID='123', show_details=False):
     ints = _predict_class(message)
     results = ints
     while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0]['intent']:
                    # set context for this intent if necessary
                    if 'context' in i:
                        if show_details: print ('context:', i['context'])
                        context[userID] = i['context']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        print("inside",results[0]['intent'])
                        response = random.choice(i['responses'])

                        response = run_commands(response,results[0]['intent'])

                        return (response)
            results.pop(0)

def main(message):
    return(_get_response(message, intents))

if __name__=="__main__":
    print("Chatbot is open\n")
    while True:
        message = input("")
        print(main(message))
###################################################################################################
import random, json , pickle, numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os,time
import hand_app
import pyjokes

os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))
intents = json.loads(open('data/intents.json').read())
lemmatizer = WordNetLemmatizer()


words = pickle.load(open('models/words.pkl', 'rb'))
classes = pickle.load(open('models/classes.pkl', 'rb'))
model = load_model('models/chatbot.h5')
context = {}
tagDict = {"terminal":"gnome-terminal", "gedit":"gedit"}

def run_commands(response,tag):
    if "incognito" in response:
        os.system("google-chrome --incognito")
        return(response)
    elif "chrome" in response:
        os.system("google-chrome")
        return(response)
    elif "chrome" in response:
        os.system("google-chrome")
        return(response)
    elif "date" in tag:
        return(response + str(time.time()))
    elif "hand_app" in tag:
        hand_app.camera()
        return(response)
    elif tag in tagDict:
        os.system(tagDict[tag])
        return(response)
    elif "joke" in tag:
        return (pyjokes.get_joke())
    else:
        return(response)
        
    
    


def _clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def _bag_of_words(sentence, words):
    sentence_words = _clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def _predict_class(sentence):
    p = _bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.95
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    if len(results)==0  and not results:
        pass
    else:
        results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list





def _get_response(message, intents, userID='123', show_details=True):
    ints = _predict_class(message)
    results = ints
    while results:
        for i in intents['intents']:
            # find a tag matching the first result
            if i['tag'] == results[0]['intent']:
                # set context for this intent if necessary
                # if 'context' in i:
                #     if show_details: print ('context:', i['context'])
                #     context[userID] = i['context']

                # check if this intent is contextual and applies to this user's conversation
                if not 'context_filter' in i or (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                    if 'context' in i:
                        if show_details: print ('context:', i['context'])
                        context[userID] = i['context']
                    
                    
                    if show_details: print ('tag:', i['tag'])
                    # a random response from the intent
                    #print("inside",results[0]['intent'])
                    response = random.choice(i['responses'])

                    #response = run_commands(response,results[0]['intent'])

                    return (response)
        results.pop(0)
    err = ["I dont know what you are talking about", "I did not understand", "are you drunk???","what do you mean??", "what does that mean??"]
    return(random.choice(err))

def main(message):
    return(_get_response(message, intents))

if __name__=="__main__":
    print("Chatbot is open\n")
    while True:
        message = input("")
        print(main(message))
        