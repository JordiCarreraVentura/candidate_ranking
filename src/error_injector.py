import random
import re
from doctest import testmod

import pandas as pd


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def introduce_typo(word: str) -> str:
    """
    Introduces a random character-level error in a word.

    Parameters
    ----------
    word: str
        A word in which we want to insert a random error.

    Return
    ------
    str
        The corrupted word with an error inserted in it.

    Examples
    --------
    >>> random.seed(3333)
    >>> assert introduce_typo("aspirin") == 'aspiin'       # deletion
    >>> random.seed(333)
    >>> assert introduce_typo("headache") == 'headagche'   # insertion
    >>> random.seed(330481)
    >>> assert introduce_typo("lung") == 'lnug'            # swap
    >>> random.seed(10663)
    >>> assert introduce_typo("lung") == 'luxg'             # substitution
    """
    typo_type = random.choice(["swap", "delete", "insert", "substitute"])

    if typo_type == "swap" and len(word) > 1:
        idx = random.randint(0, len(word) - 2)
        return word[:idx] + word[idx + 1] + word[idx] + word[idx + 2:]
    elif typo_type == "delete":
        idx = random.randint(0, len(word) - 1)
        return word[:idx] + word[idx + 1:]
    elif typo_type == "insert":
        idx = random.randint(0, len(word))
        char = random.choice(ALPHABET)
        return word[:idx] + char + word[idx:]
    elif typo_type == "substitute":
        idx = random.randint(0, len(word) - 1)
        char = random.choice(ALPHABET)
        return word[:idx] + char + word[idx + 1:]
    return word


def corrupt_text(
    text: str,
    word_error_probability: float = 0.01,
    character_error_probability: float = 0.1
) -> str:
    """
    Introduces errors in a text string based on probabilities at both the character and word level. 

    Parameters
    ----------
    text : str
        The input text string that will be corrupted.
    word_error_probability : float, optional 
        The likelihood of each word being corrupted, by default 0.2
    character_error_probability : float, optional
        The likelihood of each character being corrupted, by default 0.2

    Returns
    -------
    str
        The corrupted string with random errors inserted.

    Examples
    --------
    >>> random.seed(10663)
    >>> assert corrupt_text("take two aspirin", 0.5, 0.5) == ('keta wot aspiriz', 1, 2)
    """
    
    character_errors, word_errors = 0, 0
    while not (character_errors or word_errors):
        words = text.split()
        corrupted_words = []
        for word in words:
            corrupted_word = word
            if random.random() < word_error_probability:
                corrupted_word = ''.join(random.sample(corrupted_word, len(corrupted_word)))
                word_errors += 1
            if random.random() < character_error_probability:
                corrupted_word = introduce_typo(corrupted_word)
                character_errors += 1
            corrupted_words.append(corrupted_word)
    
    return " ".join(corrupted_words), character_errors, word_errors


testmod()