from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

import flask
from flask import Flask, request, redirect


app = Flask(__name__)


@dataclass(frozen=True)
class Person:
    name: str


NAMES = ['강승민', '이기문', '박수경', '박준영', '이승우', '신민섭']
ITEM_LIST = ['(브로슈어) 점주 앱에서 마이페이지에 가게 정보 볼 수 있도록 하기', '사용자가 어플을 사용할 때 아무 말 없이 꺼지고 끝 -> 이 아니도록 하기', '공동양육자가 아닌 다른 사람이 포인트를 선물해 줄 수 있는 기능', 'Optional 포인트 결제 전 아동이 수락할 수 있도록 하여 아무나 결제하는 것을 방지하기[보안]', '장부검색 앱에서 친절하게 안내하기', '결제에서 사칙연산 기능 추가하기', '마이페이지에서 로그아웃할 수 있도록 하기', '사용자가 실제 돈으로 앱에서 포인트 충전을 할 수 있게 하기', '가게 회원가입 함부로 열어주면 안 된다. - 요구사항 받을 내용 추가하기', '어떤 커뮤니티를 만들지 정하기', '(탑바)크레용 아이콘의 기능 추가 혹은 아이콘 삭제', '이미 가입되어있는 사용자를 앱에서 공동양육자로 통합하기', '앱 설치/회원가입하기 위한 절차를 (인터뷰용으로) 검토하기', '아이별 잔액/거래내역 확인하기 (상점용, or 학부모용)', '특정 기간의 매출내역을 볼 수 있도록 하기', '가게가 크레용에서 결제할 때, 키보드를 포스기처럼(, 000) 표시하기', '부모 회원의 홈 화면에서 아동 정보 터치 시 아동 정보로 연결', '유료 상품권 만들기', '분할 계산하기(같이 계산하기)', '마이페이지에서 가게/일반 회원 전환', '(쿠팡이츠처럼) 크레용에 등록된 가게가 앱에서 무엇이 있는지 알 수 있도록 하기', '다중 로그인이 블락하기 -> (현재는) oldest가 이상해집니다.', '아이가 갈 수 없는 가게 등록하기', '가게 주인 매출 내역 통계(그래프 등) 화면 만들기[매출 분석에 도움]', '가게 회원 결제 이후 특정 페이지로 연결', '휴대폰으로 문의할 수 있도록 앱에 전화번호/카톡 적기', 'cross platform 사용해서 ios도 같이 개발하기 (react js, flutter)', '가게회원 기본값 화면 뭘로 할까', '가입되어있지 않은 사용자를 공동양육자로 등록하기', '가게에서 하단바에 아이콘, (장부검색 등)이름 변경']
VOTES: Dict[Person, int] = dict()



"""
사람생각 정리:
    - 목표: n개의 아이템 목록에서, 최고 1개를 뽑으면 됨

과정
    - 토너먼트로 진행하려면 아이템 목록을 두개씩 짝지어야 함.
    - 짝들을 하나씩 가져와서, 사람들에게 투표를 해달라고함.
    - 만장일치가 될 때 까지 토론 (만장일치 확인은 투표 할 때 하면 됨)
    - 이후에,
    
- pick pairs from given list
- 

"""
def make_pairs(items: list) -> List[Tuple[str, Optional[str]]]]:
    pass


def vote() -> int:
    pass


def poll(pair: Tuple[str, Optional[str]]) -> int:
    vote_results = [vote for i in people]
    pass


def save_tournament_result():
    pass


def do_tournament(items: list) -> Dict[Tuple[str, Optional[str]], int]:
    item_pairs = make_pairs(items)
    winner_dict = {}
    for pair in item_pairs:
        winner_idx = poll(pair)
        winner_dict[pair] = winner_idx
    save_tournament_result()
    return winner_dict


def do_one_game(items: list) -> str:
    while len(items) > 1:
        winner_dict = do_tournament(items)
        winners = [pair[idx] for pair, idx in winner_dict.values()]
        items = winners
    assert len(items) == 1
    return items[0]

