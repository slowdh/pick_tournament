from typing import Dict
from dataclasses import dataclass
import random

DEBUG = True


@dataclass(frozen=True)
class Person:
    name: str
    path: str


def read_and_report() -> Dict[Person, int]:
    votes: Dict[Person, int] = dict()

    if DEBUG:
        for person in people:
            votes[person] = random.randint(1, 2)
    else:
        for vote in votes:
            with open(vote['path']) as f:
                vote['target'] = None

    print('Report::::')
    for person in people:
        if person in votes:
            print(f"{person.name} vote: {votes[person]}")
        else:
            print(f'{person.name} didn"t vote')
    return votes


def run_match() -> int:
    votes = dict()
    is_unanimous = False
    while not is_unanimous:
        votes = read_and_report()
        is_unanimous = (len(set(votes.values())) == 1)
    else:
        assert len(votes) > 0
        return next(iter(votes.values()))


if __name__ == '__main__':
    names = ['DH Kim', 'GM lee', 'JW Kim']
    people_file_paths = ['dh_path.txt', 'gm_path.txt', 'jw_path.txt']
    people = [Person(name, path) for name, path in zip(names, people_file_paths)]
    run_match()
