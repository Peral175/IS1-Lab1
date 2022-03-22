import re, csv, random
from datetime import datetime

CHATLOG = "chatLog.txt"             # constant -> file name for chat log

psychobable = [
   [r'W|what time is it in (.*)\s?\??',
      ["The current time in {location} is: {time}.",
      "In {location} it is {time}."
      ]
   ],

   [r'W|what time is it\s?\??',
      ["The current time is: {time}.",
      "It is {time}."
      ]
   ],

   [r'P|put a (.*) alarm\?!',
      [
        "Setting a {timer} alarm.",
        "Alarm set for {timer}",
        "..."
      ]
   ],

   [r'S|set a (.*) alarm\?!',
      [
        "Setting a {timer} alarm.",
        "Alarm set for {timer}",
        "..."
      ]
   ],

   [r'C|can you give me the time in (.*)\?.',
      [
        "The time in {location} is {time}"
      ]
   ],

   [r'A|activate a (.*) timer',
      [
        "Timer activated."
      ]
   ],

   [r'(.*)',
      [
         "Sorry I can't help you with that."
         "There seems to be a issue with your request."
         "Sorry I do not understand your request...",
         "I do not know what you are asking of me...",
         "I am unable to understand what you mean by that."
      ]
   ]
]

class Eliza:
    def __init__(self):
        # initialization of class Eliza with empty lists
        self.initials = []      # list of greetings of the chatbot
        self.finals = []        # list of final words of the chatbot
        self.quits = []         # list of words to quit talking to the chatbot
    
    def load(self, filePath):
        # method load
        # parameters: self 
        #             filePath -> file containing initials, finals and quits
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
        # method by which Eliza responds
        # parameters:   self,
        #               text    -> some input by user
        # retuns:       output  -> some response by Eliza based on psychobable
        output = None
        if text.lower() in self.quits:  # to quit 
            return output
        output = self.analyze(text)     # analyze text and respond accordingly
        return output

    def analyze(self, statement):
        # method to analyze the user input
        # parameters:   self,
        #               statement   -> user input
        # returns:      responds    ->  based on psychobable
        
        for pattern, responses in psychobable:
            match = re.match(pattern, statement)        # match user input with psychobable regex
            if match:
                response = random.choice(responses)     # respond with one of the possible responses
                zone = 'Luxembourg'                     # zone default is Luxembourg
                alarm = '0 seconds'                     # alarm default is 0 seconds
                for g in match.groups():
                    if containsDigit(g):                # determine if the user wants to set an alarm or know the time
                        alarm = g
                    else:
                        zone = g
                return response.format(time=getLocalTime(zone), location=zone, timer=alarm)

    def run(self):
        # method to converse with the user
        # loop is broken with key quit words
        # method records conversation in a chatlog
        initial = self.randInitial()        # start conversation with a greeting  
        file = open(CHATLOG, 'w')
        file.write('Bot: \t' + initial)     # Currently we override the file at each program execution
        file.close()       
        print(initial)                      # print greeting on console
        while True:                         # wait for user reply
            sent = input('> ')
            logChat(CHATLOG,sent,'Human: ')
            output = self.respond(sent)     # determine what to respond
            if output is None:
                break
            print(output)
            logChat(CHATLOG,output, 'Bot: ')
        final = self.randFinal()            # Terminate the conversation with a goodbye
        print(final) 
        logChat(CHATLOG,final, 'Bot: ')

def containsDigit(string):
    # function to determine if a given string contains a number
    # returns true if string contains at least one digit else false
    for character in string:
        if character.isdigit():
            return True
    return False

def getLocalTime(zone):
    # function to get UTC-time and 
    # add the timezone delta extracted of a given zone from a csv file to it.
    # returns local time for a given zone/city, 
    # expressed in hours:minutes:seconds
    with open("timeZone.csv",'r',newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        utcDelta = 0                        # default delta
        utcTime = datetime.utcnow().time()  # current UTC-time
        for row in reader:
            if zone == row[0]:              # match first csv argument with given zone
                utcDelta = row[1]           # extract delta from file
        return '{H}:{M}:{S}'.format(H = str((int(utcTime.hour) + int(utcDelta))%24).zfill(2), M = str(utcTime.minute).zfill(2), S = str(utcTime.second).zfill(2))  # add delta to UTC-time

def logChat(filePath, line, actor):
    # method logChat
    # attributes: 
    #               filePath    -> where to save the conversation, 
    #               line        -> line to be saved, 
    #               actor       -> defines which actor said line
    with open(filePath, 'a') as file:
        file.write('\n'+actor+'\t'+line)

def main():
    eliza = Eliza()                     # initialize the class with empty values
    eliza.load('initialsFinals.txt')    # load initials, finals and quit keywords
    eliza.run()                         # run Eliza chatbot

if __name__ == '__main__':
    main()