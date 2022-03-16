import re, csv, random
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
        output = self.analyze(text)
        return output

    def getUTCTime(self, zone):
        with open("timeZone.csv",'r',newline='\n') as csvfile:
            reader = csv.reader(csvfile)
            utcDelta = 0
            utcTime = datetime.utcnow().time()
            for row in reader:
                if zone == row[0]: 
                    utcDelta = row[1]
            return '{H}:{M}:{S}'.format(H = str(int(utcTime.hour) + int(utcDelta)), M = utcTime.minute, S = utcTime.second)

    def analyze(self, statement):
        for pattern, responses in psychobable:
            match = re.match(pattern, statement)
            if match:
                response = random.choice(responses)
                zone = 'Luxembourg'
                alarm = '0 seconds'
                for g in match.groups():
                    if self.containsDigit(g):
                        alarm = g
                    else:
                        zone = g
                return response.format(time=self.getUTCTime(zone), location=zone, timer=alarm)
    
    def containsDigit(self, string):
        for character in string:
            if character.isdigit():
                return True
            return False

    def logChat(self, filePath, line, actor):
        # method logChat
        # attributes:   self, 
        #               filePath    -> where to save the conversation, 
        #               line        -> line to be saved, 
        #               actor       -> which actor said line
        with open(filePath, 'a') as file:
            file.write('\n'+actor+'\t'+line)
            # file.close()  Not need within this "with" block

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

psychobable = [[r'What time is it in (.*)\?',
     ["The current time in {location} is: {time}",
     ]
    ],
    [r'What time is it ?',
     ["The current time is: {time}"
     ]
    ],
   
    [r'Put a (.*) alarm!',
     [
        "Setting an {timer} alarm.",  
        "Alarm set for {timer}",
     ]
    ]
]

def main():
    eliza = Eliza()             # initialize the class with empty values
    eliza.load('textFile.txt')  # load values
    eliza.run()                 # run Eliza chatbot

if __name__ == '__main__':
    main()
