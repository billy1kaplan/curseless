import random


try:
    with open('/usr/share/dict/cracklib-small') as f:
        words = [word.strip() for word in f.readlines()]
        alpha_words = [word for word in words if word.isalpha()]
except Exception:
    alpha_words = ['some',
                   'great',
                   'fruits',
                   'are',
                   'banana',
                   'tomato',
                   'kiwi']


def choose_word():
    return random.choice(alpha_words)
