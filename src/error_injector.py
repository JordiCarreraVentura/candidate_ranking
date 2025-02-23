import random
import re
from doctest import testmod

import pandas as pd


ALPHABET = "abcdefghijklmnopqrstuvwxyz"

ERROR_TYPES = ["swap", "delete", "insert", "substitute"]


def random_word() -> str:
    return "".join(random.sample(ALPHABET, random.randrange(4, 10)))


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
    typo_type = random.choice(ERROR_TYPES)

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
    word_error_probability: float = 0.1,
    character_error_probability: float = 0.1
) -> str:
    """
    Introduces errors in a text string or string list based on probabilities
    at both the character and word level.

    Parameters
    ----------
    text: str
        The input text string that will be corrupted.
    character_error_probability: float = 0.1
        The likelihood of each character being corrupted. Defaults to 0.1
    word_error_probability: float = 0.1
        The likelihood of each word being corrupted. Defaults to 0.1

    Returns
    -------
    Tuple[str, int, int]
        The corrupted string with random errors inserted along with
        the number of character-level errors and word-level errors
        introduced in it.

    Examples
    --------
    >>> random.seed(10663)
    >>> corrupt_text("take two aspirin", 0.5, 0.5)
    ('tnake two aspirinq', 2, 0)

    >>> random.seed(11136)
    >>> corrupt_text("take two aspirin", character_error_probability=0.77, word_error_probability=0)
    ('takeq tow aspirin', 2, 0)

    >>> random.seed(11136)
    >>> corrupt_text("take two aspirin", character_error_probability=0.0, word_error_probability=0.5)
    ('taketwo aspirin', 0, 1)

    >>> random.seed(4489484)
    >>> corrupt_text("take two aspirin", character_error_probability=0.0, word_error_probability=0.5)
    ('two aspirin', 0, 1)

    >>> random.seed(448)
    >>> corrupt_text("take two aspirin", character_error_probability=0.0, word_error_probability=0.5)
    ('take aspirin two', 0, 1)
    """

    character_errors, word_errors = set([]), 0

    while not (len(character_errors) or word_errors):

        words = text.split()
        corrupted_tokens = []
        for idx, word in enumerate(words):
            corrupted_word = word
            if character_error_probability and random.random() < character_error_probability:
                corrupted_word = introduce_typo(corrupted_word)
                character_errors.add(idx)
            corrupted_tokens.append(corrupted_word)
    
        if random.random() < word_error_probability:
            error_type = random.choice(ERROR_TYPES + ['merge'])
            idx = random.choice(list(
                set(range(len(corrupted_tokens) - 1))
                - character_errors
            ))
            if error_type == 'delete':
                corrupted_tokens = corrupted_tokens[:idx] + corrupted_tokens[idx + 1:]
                word_errors += 1
            elif error_type == 'substitute':
                corrupted_tokens[idx] = random_word()
                word_errors += 1
            elif error_type == 'swap':
                corrupted_tokens = (
                    corrupted_tokens[:idx]
                    + [corrupted_tokens[idx + 1]]
                    + [corrupted_tokens[idx]]
                    + corrupted_tokens[idx + 2:]
                )
                word_errors += 1
            elif error_type == 'merge':
                corrupted_tokens = (
                    corrupted_tokens[:idx]
                    + [f"{corrupted_tokens[idx]}{corrupted_tokens[idx + 1]}"]
                    + corrupted_tokens[idx + 2:]
                )
                word_errors += 1
            elif error_type == 'insert':
                corrupted_tokens = (
                    corrupted_tokens[:idx] 
                    + [random_word()]
                    + corrupted_tokens[idx + 1:]
                )
                word_errors += 1
    
    return " ".join(corrupted_tokens), len(character_errors), word_errors


testmod()