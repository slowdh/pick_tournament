from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random

import flask
from flask import Flask, request, redirect


# init is needed
app = Flask(__name__)


DEBUG = True


@dataclass(frozen=True)
class Person:
    name: str
    path: str

NAMES = ['1', '2', '3', '4', '5', '6']
PATHS = [None for _ in range(6)]
VOTES: Dict[Person, int] = dict()
PEOPLE: Dict[str, Person] = {NAMES[i]: Person(NAMES[i], PATHS[i]) for i in range(6)}


def read_and_report(people: List[Person]) -> Dict[Person, int]:
    if DEBUG:
        for person in people:
            VOTES[person] = random.randint(1, 2)
    else:
        for vote in VOTES:
            with open(vote['path']) as f:
                vote['target'] = None

    print('Report::::')
    for person in people:
        if person in VOTES:
            print(f"{person.name} vote: {VOTES[person]}")
        else:
            print(f'{person.name} didn"t vote')
    return VOTES


def run_match() -> int:
    votes = dict()
    is_unanimous = False
    while not is_unanimous:
        votes = read_and_report()
        is_unanimous = (len(set(votes.values())) == 1)
    else:
        assert len(votes) > 0
        return next(iter(votes.values()))


def get_match_list() -> List:
    match_list = ['sample1', 'sample2', 'sample3']
    return match_list


def get_binary_pairs(items: list) -> List[Tuple[str, Optional[str]]]:
    binary_pairs = []
    while len(items) > 0:
        pair = items[:2]

        if len(pair) == 1:
            pair.append(None)
        assert len(pair) == 2
        binary_pairs.append(tuple(pair))

        items = items[2:]
    return binary_pairs


assert get_binary_pairs(list(range(10))) == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
assert get_binary_pairs(list(range(1))) == [(0, None)]
assert get_binary_pairs(list(range(0))) == []



def write_vote(vote: Tuple[Person, int], votes: Dict[Person, int]):
    person, target = vote
    votes[person] = target


@app.route('/vote')
def read_vote():
    user_name = request.args.get('user_name', '')
    vote = request.args.get('vote', '')
    VOTES[PEOPLE[user_name]] = vote
    return redirect(flask.url_for('show_current_poll_status'))


@app.route('/votes')
def show_current_poll_status():
    poll_status = []
    for person, vote in VOTES.items():
        poll_status.append(f"{person.name}: {vote}")
    return '<br>'.join(poll_status)


@app.route('/clear')
def clear_poll_results():
    global VOTES
    VOTES = dict()
    return redirect(flask.url_for('show_current_poll_status'))
