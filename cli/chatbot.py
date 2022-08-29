"""
A command line interface to run the chatbot locally.
"""
import logging
import re
import sys
import spacy
from spacy.tokens import Doc as SpacyDoc
from collections import Counter
from nltk import pos_tag as nltk_pos_tag
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from typing import List


class ChatBot:
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    stopwords = set(nltk_stopwords.words("english"))
    word2vec = spacy.load("en_core_web_sm")

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
        msg = re.sub(r'[^\w\s]', '', msg)  # remove punctuation
        tokens = nltk_word_tokenize(msg)
        # remove stopwords
        tokens = [token for token in tokens if token not in self.stopwords]
        logging.debug("tokens: [%s]", tokens)
        return tokens

    def __compare_bow(self, bow_user_msg: Counter, bow_response: Counter) -> float:
        """Return the similarity of the user message and the response."""
        return sum([bow_user_msg[token] for token in bow_user_msg if token in bow_response]) / len(bow_user_msg)

    def __compute_similarity(self, tokens: List[SpacyDoc], category: SpacyDoc) -> List[float]:
        """Return a list of similarities between the tokens and the category."""
        return [[token.text, category.text, token.similarity(category)] for token in tokens]

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
        processed_responses = [self.__preprocess(
            response) for response in self.responses]
        similarity_list = [self.__compare_bow(
            bow_user_msg, bow_response) for bow_response in processed_responses]
        return self.responses[similarity_list.index(max(similarity_list))]

    def find_entities(self, user_msg: str) -> str:
        """Return a list of entities in the user message."""
        tagged_user_msg = nltk_pos_tag(user_msg.split())
        logging.debug("tagged_user_msg: [%s]", tagged_user_msg)

        msg_nouns = [word for word,
                     tag in tagged_user_msg if tag == "NNP"]  # NNP: Proper noun, singular
        logging.debug("msg_nouns: [%s]", msg_nouns)

        tokens = self.word2vec(" ".join(msg_nouns))
        category = self.word2vec("city")

        word2vec_result = self.__compute_similarity(tokens, category)
        word2vec_result.sort(key=lambda x: x[2], reverse=True)
        logging.debug("word2vec_result: [%s]", word2vec_result)

        return word2vec_result[0][0]

    def respond(self, user_msg: str) -> str:
        """Return a response to the user message."""
        if self.make_exit(user_msg):
            return "Bye!"
        else:
            best_response = self.find_intent_match(user_msg)
            entity = self.find_entities(user_msg)
            return best_response.format(entity, "", "")


if __name__ == "__main__":
    # Doctest
    import doctest
    doctest.testmod()
    ###

    # Logging
    import logging
    logging.basicConfig(filename="chatbot.log", level=logging.DEBUG)
    ###

    responses = []

    # optional command line argument to load responses from a file
    if len(sys.argv) > 1:
        responses_file = sys.argv[1]
        with open(responses_file, "r") as f:
            responses = f.read().splitlines()

    bot = ChatBot(responses)
    while True:
        user_msg = input("Enter your message: ")
        print(bot.respond(user_msg))
        if bot.make_exit(user_msg):
            break
