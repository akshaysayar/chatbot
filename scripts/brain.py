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

                    response = run_commands(response,results[0]['intent'])

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
        