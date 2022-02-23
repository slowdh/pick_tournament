from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random
import time

import flask
from flask import Flask, request, redirect


# init is needed
app = Flask(__name__)


@dataclass(frozen=True)
class Person:
    name: str
    path: str


DEBUG = True
SLEEP_TIME = 0
NAMES = ['a', 'b', 'c', 'd', 'e', 'f']
ITEM_LIST = ['1', '2', '3', '4', '5']
PATHS = [None for _ in range(6)]
VOTES: Dict[Person, int] = dict()
PEOPLE: Dict[str, Person] = {NAMES[i]: Person(NAMES[i], PATHS[i]) for i in range(6)}
CURRENT_MATCH = ()
MATCH_HISTORY = []


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


@app.route('/history')
def show_match_history():
    return '<br>'.join(MATCH_HISTORY)


@app.route('/')
def show_current_items():
    return '<br>'.join(ITEM_LIST)


@app.route('/match')
def show_current_match():
    match_list_with_number = [f"[{i + 1}]: {CURRENT_MATCH[i]}" for i in range(len(CURRENT_MATCH))]
    match_list_with_number.append(f"[3]: 중립")
    return '<br>'.join(match_list_with_number)


@app.route('/vote')
def read_vote():
    user_name = request.args.get('user_name', '')
    vote = request.args.get('vote', '')
    VOTES[PEOPLE[user_name]] = vote
    # todo: change it
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


def read_and_report(people: List[Person]) -> Dict[Person, int]:
    if DEBUG:
        for person in people:
            VOTES[person] = random.randint(1, 2)
    else:
        pass

    print('Report::::')
    for person in people:
        if person in VOTES:
            print(f"{person.name} vote: {VOTES[person]}")
        else:
            print(f'{person.name} didn"t vote')
    return VOTES


def write_vote(vote: Tuple[Person, int], votes: Dict[Person, int]):
    person, target = vote
    votes[person] = target


def run_match(binary_pair: Tuple[str, Optional[str]]) -> int:
    global VOTES
    VOTES = dict()
    if None in binary_pair:
        not_none_idx = [i for i in range(len(binary_pair)) if binary_pair[i] is not None][0]
        assert binary_pair[not_none_idx] is not None
        return not_none_idx + 1

    is_unanimous = False
    while not is_unanimous:
        VOTES = read_and_report(PEOPLE.values())
        is_unanimous = (len(set(VOTES.values())) == 1)
        time.sleep(SLEEP_TIME)
    else:
        assert len(VOTES) > 0
        return next(iter(VOTES.values()))


#todo: save history with json file
def save_history(save_path: str):
    pass


def run_round(binary_pairs: List[Tuple[str, Optional[str]]]):
    winner_list = []
    for binary_pair in binary_pairs:
        global CURRENT_MATCH, MATCH_HISTORY
        CURRENT_MATCH = binary_pair
        match_winner = run_match(binary_pair)
        MATCH_HISTORY.append(', '.join([f"[{match_winner}]"] + list(map(str, binary_pair))))
        winner_list.append(binary_pair[match_winner - 1])
        input('Press any key to go next match.')
    MATCH_HISTORY.append('<br>')
    return winner_list


@app.route('/run')
def run_game():
    global ITEM_LIST
    item_list = ITEM_LIST
    while len(item_list) > 1:
        random.shuffle(item_list)
        binary_pairs = get_binary_pairs(item_list)
        winner_list = run_round(binary_pairs)
        item_list = winner_list
    winner = item_list[0]
    ITEM_LIST = ITEM_LIST.remove(winner)
    return redirect(flask.url_for('show_match_history'))
