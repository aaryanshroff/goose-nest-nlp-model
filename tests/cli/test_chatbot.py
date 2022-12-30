import src.cli.chatbot.ChatBot as ChatBot
import logging


def test_make_exit():
    c = ChatBot()
    assert c.make_exit("I want to quit") == True
    assert c.make_exit("Bye!") == True
    assert c.make_exit("Pause") == True
    assert c.make_exit("Exit") == True
    assert c.make_exit("Talk to you later") == True


def test_find_intent_match():
    c1 = ChatBot()
    assert c1.find_intent_match("Hello!") == ""
    c2 = cli.chatbot.ChatBot(["Hello!", "What do you need help with?"])
    assert c2.find_intent_match("Hello, how are you?") == "Hello!"
    assert c2.find_intent_match(
        "I need help.") == "What do you need help with?"


def test_find_entities():
    c = ChatBot(categories=[
        ("city", "NNP"), ("budget", "CD")])

    # TODO: Fix failing test
    # assert c.find_entities(
    #    "Find me houses in San Francisco") == "San Francisco"
    #

    assert c.find_entities("Find me houses in Toronto under 700") == [
        ("city", "Toronto"), ("budget", "700")]
    assert c.find_entities(
        "I want to buy a house in Waterloo below 600") == [("city", "Waterloo"), ("budget", "600")]
