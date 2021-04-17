import random, json, pickle, numpy as np, os
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

def main():
    os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))
    
    lemmatizer = WordNetLemmatizer()

    intents = json.loads(open('data/intents.json').read())

    words = []
    classes= []
    documents = []
    ignore_letters = ['?', ':', '.', ',']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            wordlist = word_tokenize(pattern)
            words.extend(wordlist)
            documents.append((wordlist, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    print(documents)

    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
    words = sorted(set(words))

    classes = sorted(set(classes))


    training = []
    output_empty = [0] * len(classes)

    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

    print(output_row)


    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

    model.save("models/chatbot.h5", hist)
    pickle.dump(words, open('models/words.pkl', 'wb'))
    pickle.dump(classes, open('models/classes.pkl', 'wb'))


if __name__=="__main__":
    main()