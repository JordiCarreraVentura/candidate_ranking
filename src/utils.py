import os
import sys
from typing import Any

def autoconfigure() -> str:
    curr_dir = os.path.realpath(__file__)
    while os.path.basename(curr_dir) != "candidate_ranking":
        curr_dir = os.path.dirname(curr_dir)
    sys.path.append(curr_dir)
    return curr_dir

def from_txt(path: str) -> str:
    with open(path, 'r') as rd:
        return rd.read()

def positive_case(x: Any) -> int:
    return 1

def negative_case(x: Any) -> int:
    return 0

def zero(x: Any) -> int:
    return 0