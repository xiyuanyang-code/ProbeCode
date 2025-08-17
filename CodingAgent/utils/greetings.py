# generate random greetings for code
import random
from typing import List

WELCOME_GREETINGS = [
    "Welcome! This is ProbeCode, what can I do for you?",
    "Hello there. Ready to dive into some code?",
    "ProbeCode online. What's on your mind?",
    "Greetings. I'm here to help you navigate your code.",
    "Hey! ProbeCode is ready for your commands.",
    "Welcome. Let's get to the bottom of this code together.",
    "Access granted. Let's begin the analysis.",
    "Ready to solve some puzzles? ProbeCode is at your service.",
    "Welcome back. Your code analysis assistant is here.",
    "Hello. How can I assist with your coding project?",
]

GOODBYE_GREETINGS = [
    "Goodbye!",
    "See you later!",
    "Until next time. Stay curious!",
    "Happy coding!",
    "ProbeCode signing off. Goodbye!",
    "Mission accomplished. Farewell!",
    "I'll be here if you need me again.",
    "Take care and have a great day.",
    "Analysis complete. Come back anytime.",
    "Goodbye for now. Your code is in good hands.",
]


def _generate_random(sentences: List[str]):
    length = len(sentences)
    return sentences[random.randint(0, length - 1)]

def welcome():
    return _generate_random(WELCOME_GREETINGS)

def goodbye():
    return _generate_random(GOODBYE_GREETINGS)
