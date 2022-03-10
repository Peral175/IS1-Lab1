import re
import random
from datetime import datetime

CHATLOG = "chatLog"

class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
    
    def load(self, filePath):
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
        return random.choice(self.initials)
    
    def randFinal(self):
        return random.choice(self.finals)
    
    def respond(self, text):
        output = None
        if text.lower() in self.quits: # to quit 
            return output
        output = text
        return output

    def logChat(self, filePath, line, actor):
        with open(filePath, 'a') as file:
            file.write('\n'+actor+'\t'+line)
            file.close()

    def run(self):
        initial = self.randInitial()
        file = open(CHATLOG, 'w')
        file.write('Bot: \t' + initial) # Erase content from previous chat?
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
    eliza = Eliza()
    eliza.load('textFile.txt')
    eliza.run()

if __name__ == '__main__':
    main()
