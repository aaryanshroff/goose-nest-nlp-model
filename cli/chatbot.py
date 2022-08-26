"""
A command line interface to run the chatbot locally.
"""
import re
from collections import Counter
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from typing import List


class ChatBot:
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    stopwords = set(nltk_stopwords.words("english"))

    def __init__(self, responses=None):
        """Initialize the chatbot with a list of responses.
        >>> c1 = ChatBot()
        >>> c1.responses
        []
        >>> c2 = ChatBot(["Hello!"])
        >>> c2.responses
        ['Hello!']
        """
        self.responses = responses or []

    def __preprocess(self, msg: str) -> List[str]:
        """Preprocess the message to remove punctuation and tokenize."""
        msg = msg.lower()
        msg = re.sub(r'[^\w\s]', '', msg) # remove punctuation
        tokens = nltk_word_tokenize(msg)
        tokens = [token for token in tokens if token not in self.stopwords] # remove stopwords
        return tokens
    
    def __compare_bow(self, bow_user_msg: Counter, bow_response: Counter) -> float:
        """Return the similarity of the user message and the response."""
        return sum([bow_user_msg[token] for token in bow_user_msg if token in bow_response]) / len(bow_user_msg)
    
    def make_exit(self, user_msg: str) -> bool:
        """Return true if the user wants to exit the chatbot.
        
        >>> c = ChatBot()
        >>> c.make_exit("I want to quit")
        True
        >>> c.make_exit("Bye!")
        True 
        """
        processed_msg = user_msg.lower()
        for exit_command in self.exit_commands:
            if exit_command in processed_msg:
                return True 
        return False
    
    def find_intent_match(self, user_msg: str) -> str:
        """Return the intent that matches the user message."""
        if self.responses == []:
            return ""
        bow_user_msg = Counter(self.__preprocess(user_msg))
        processed_responses = [self.__preprocess(response) for response in self.responses]
        similarity_list = [self.__compare_bow(bow_user_msg, bow_response) for bow_response in processed_responses]
        return self.responses[similarity_list.index(max(similarity_list))]

        
    
    def respond(self, user_msg: str) -> str:
        """Return a response to the user message."""
        if self.make_exit(user_msg):
            return "Bye!"
        else:
            return "I don't know what you mean."
    

if __name__ == "__main__":
    ###
    import doctest
    doctest.testmod()
    ###
    bot = ChatBot()
    while True:
        user_msg = input("Enter your message: ")
        print(bot.respond(user_msg))
        if bot.make_exit(user_msg):
            break