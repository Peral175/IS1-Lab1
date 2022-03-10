import re
import random
from datetime import datetime

CHATLOG = "chatLog.txt"             # file name for chat log

class Eliza:
    def __init__(self):
        self.initials = []      # list of greetings of the chatbot
        self.finals = []        # list of final words of the chatbot
        self.quits = []         # list of words to quit talking to the chatbot
    
    def load(self, filePath):
        # method load
        # parameters: self, filePath -> file containing initials, finals and quits
        with open(filePath) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)

    def randInitial(self):
        # return random initial
        return random.choice(self.initials)
    
    def randFinal(self):
        # return random final
        return random.choice(self.finals)
    
    def respond(self, text):
        # ...
        output = None
        if text.lower() in self.quits: # to quit 
            return output
        output = text
        return output

    def logChat(self, filePath, line, actor):
        # method logChat
        # attributes:   self, 
        #               filePath    -> where to save the conversation, 
        #               line        -> line to be saved, 
        #               actor       -> which actor said line
        with open(filePath, 'a') as file:
            file.write('\n'+actor+'\t'+line)
            file.close()

    def run(self):
        initial = self.randInitial()        
        file = open(CHATLOG, 'w')           
        file.write('Bot: \t' + initial)     # Erase content from previous chat?
        file.close()       
        print(initial)
        while True:
            sent = input('> ')
            self.logChat(CHATLOG,sent,'Human: ')
            output = self.respond(sent)
            if output is None:
                break
            print(output)
            self.logChat(CHATLOG,output, 'Bot: ')
        final = self.randFinal()
        print(final) 
        self.logChat(CHATLOG,final, 'Bot: ')

def getTime():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    return current_time

psychobable = [
    [r'What time(.*)\?',
    ['The current time is: {0} in {1}',
    ]]
]

def main():
    eliza = Eliza()             # initialize the class with empty values
    eliza.load('textFile.txt')  # load values
    eliza.run()                 # run Eliza chatbot

if __name__ == '__main__':
    main()
