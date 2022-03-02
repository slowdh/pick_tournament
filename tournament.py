from typing import List, Tuple, Optional

import flask
from flask import Flask
from flask import request, redirect


NAMES = ['dh', 'jw']
ITEMS = ['Clean up house', 'Make cake', 'Learn how to program', 'Search for movie to watch', 'Call friend']
ROUND_MATCHES: List[Tuple[str, Optional[str]]] = []
CURRENT_MATCH = ()
HISTORY: List[List[List[Tuple[Tuple[str, Optional[str]], Optional[int]]]]] = []
VOTES = {}


def get_current_game_history():
    return HISTORY[-1]


def get_current_round_history():
    return HISTORY[-1][-1]


def get_binary_pairs(items: List[str]) -> List[Tuple[str, Optional[str]]]:
    binary_pairs = []
    while len(items) > 0:
        pair = items[:2]
        if len(pair) == 1:
            pair.append(None)
        binary_pairs.append(tuple(pair))
        items = items[2:]
    return binary_pairs


def prepare_new_round(items):
    global ROUND_MATCHES, CURRENT_MATCH
    assert len(ROUND_MATCHES) == 0
    ROUND_MATCHES = get_binary_pairs(items)
    CURRENT_MATCH = ROUND_MATCHES.pop(0)
    get_current_game_history().append([])


def prepare_new_game():
    global ROUND_MATCHES
    if len(ITEMS) > 0:
        HISTORY.append([])
        prepare_new_round(items=ITEMS)
    else:
        print("End of game")


prepare_new_game()


app = Flask(__name__)


@app.route("/")
def show_current_status():
    poll_result = [f"{name}: {vote}" for name, vote in VOTES.items()]
    if CURRENT_MATCH is not None:
        current_match_with_index = [f"[{idx}] {item}" for idx, item in enumerate(CURRENT_MATCH)]
    else:
        current_match_with_index = []
    return f"Match: <p>{'<p>'.join(current_match_with_index)}<p>{'<p>'.join(poll_result)}"


@app.route("/items")
def show_items():
    return "<p>".join(ITEMS)


@app.route("/vote")
def read_vote():
    global CURRENT_MATCH, ROUND_MATCHES, VOTES
    user_name = request.args.get('user_name', '')
    vote = request.args.get('vote', '')
    VOTES[user_name] = vote

    if len(VOTES) == len(NAMES) and len(set(VOTES.values())) == 1:
        winner_index = int(next(iter(VOTES.values())))
        get_current_round_history().append((CURRENT_MATCH, winner_index))
        VOTES = {}
        if len(ROUND_MATCHES) > 0:
            CURRENT_MATCH = ROUND_MATCHES.pop(0)
        else:
            wrap_up_round()
    return redirect(flask.url_for('show_current_status'))


def wrap_up_round():
    remained_items = [match[winner_index] for match, winner_index in get_current_round_history()]
    if len(remained_items) == 1:
        winner_item = remained_items[0]
        ITEMS.remove(winner_item)
        prepare_new_game()
    else:
        prepare_new_round(remained_items)


@app.route("/votes")
def show_poll_result():
    poll_status = []
    for name, vote in VOTES.items():
        poll_status.append(f"{name}: {vote}")
    return '<p>'.join(poll_status)


@app.route('/history')
def show_history():
    return '<p>'.join([str(item) for item in HISTORY])
