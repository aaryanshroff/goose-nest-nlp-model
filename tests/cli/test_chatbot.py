import cli.chatbot

def test_make_exit():
    c = cli.chatbot.ChatBot()
    assert c.make_exit("I want to quit") == True
    assert c.make_exit("Bye!") == True
    assert c.make_exit("Pause") == True
    assert c.make_exit("Exit") == True
    assert c.make_exit("Talk to you later") == True

def test_find_intent_match():
    c1 = cli.chatbot.ChatBot()
    assert c1.find_intent_match("Hello!") == ""
    c2 = cli.chatbot.ChatBot(["Hello!", "What do you need help with?"])
    assert c2.find_intent_match("Hello, how are you?") == "Hello!"
    assert c2.find_intent_match("I need help.") == "What do you need help with?"
