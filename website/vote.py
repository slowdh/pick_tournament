from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import time

import flask
from flask import Flask, request, redirect

from data import NAMES, ITEMS


app = Flask(__name__)


# python
@dataclass(frozen=True)
class Person:
    name: str


VOTES: Dict[Person, int] = dict()
PEOPLE: List[Person] = [Person(name) for name in NAMES]
CURRENT_PAIR = ()
TOURNAMENT_RESULT = []


def make_pairs(items: list) -> List[Tuple[str, Optional[str]]]:
    pairs = []
    while len(items) > 1:
        pair = items[:2]
        if len(pair) == 1:
            pair.append(None)
        pairs.append(tuple(pair))
        items = items[2:]
    return pairs


def get_unanimous_poll() -> int:
    while not (len(VOTES) == len(PEOPLE) and len(set(VOTES.values())) == 1):
        pass
    return next(iter(VOTES.values()))


def save_tournament_result(winner_dict: Dict[Tuple[str, Optional[str]], int]):
    TOURNAMENT_RESULT.append(winner_dict)
    pass


def run_tournament(items: list) -> Dict[Tuple[str, Optional[str]], int]:
    item_pairs = make_pairs(items)
    winner_dict = {}
    for pair in item_pairs:
        global CURRENT_PAIR
        CURRENT_PAIR = pair
        if None in pair:
            winner_idx = 0
            assert pair[1] == None
        else:
            winner_idx = get_unanimous_poll()
        winner_dict[pair] = winner_idx
    save_tournament_result()
    return winner_dict


def run_one_game(items: list) -> str:
    while len(items) > 1:
        winner_dict = run_tournament(items)
        winners = [pair[idx] for pair, idx in winner_dict.values()]
        items = winners
    assert len(items) == 1
    return items[0]


# flask URLS
@app.route('/')
def show_items():
    return '<br>'.join(ITEMS)


@app.route('/vote')
def get_vote():
    user_name = request.args.get('user_name', '')
    vote = request.args.get('vote', '')
    person = [p for p in PEOPLE if p.name == user_name][0]
    VOTES[person] = vote
    return redirect(flask.url_for('show_current_poll_status'))


@app.route('/votes')
def show_current_poll_status():
    poll_status = []
    for person, vote in VOTES.items():
        poll_status.append(f"{person.name}: {vote}")
    return '<br>'.join(poll_status)


@app.route('/match')
def show_current_match():
    current_pair = list(map(str, CURRENT_PAIR))
    pair_with_idx = [f"[{i}]: {current_pair[i]}" for i in range(len(current_pair))]
    pair_with_idx.append(f"[3]: 중립")
    return '<br>'.join(pair_with_idx)


@app.route('/history')
def show_tournament_history():
    return tuple(TOURNAMENT_RESULT)


@app.route('/run')
def run_game():
    global ITEMS
    winner_item = run_one_game(ITEMS)
    ITEMS = ITEMS.remove(winner_item)
    return redirect(flask.url_for(show_tournament_history))
