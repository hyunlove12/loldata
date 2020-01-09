import requests
import datetime
import sys
import json

sys.path.append('./data/key_config.json')
import config

if __name__ == '__main__':
    # 아이디에 대한 기본 정보 가져오기
    f = open('./data/key_config.json', 'r')
    js = json.loads(f.read())
    api_key = js['apiKey']
    #hd = js['headers']
    nick_name = ""
    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + nick_name
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": api_key,
        "X-Riot-Token": api_key,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
            }
    # 반환값이 무엇인지..?
    res = requests.get(url=url, headers=headers)
    # accountId
    acc_id = res.json()['accountId']
    # 매치 정보 가져오기
    # beginIndex -> default : 0 / max값은 totalmatch - 1
    # endIndex
    # 범위는 100을 초과할 수 없으며, endIndex가 없으면 100단위로 설정
    url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?beginIndex={}'.format(acc_id,0)
    res = requests.get(url=url, headers=headers)
    print(res.json())
    result = res.json()
    #print(res.json()['endIndex'])
    #print(res.json()['startIndex'])
    print(result['totalGames'])
    print(result['matches'][0]['gameId'])
    print(result['matches'][0]['role'])
    print(result['matches'][0]['season'])
    match_id = result['matches'][0]['gameId']

    # match별 게임 정보
    url = 'https://kr.api.riotgames.com/lol/match/v4/matches/{}'.format(match_id)
    res = requests.get(url=url, headers=headers)
    print(res.json())
    match_result = res.json()
    # 반복문 돌려서 해당 플레이어의 id 가져오기
    for i in match_result['participantIdentities']:
        if i['player']['summonerName'] == '봉익천상':
            part_id = i['participantId']
            matchHistoryUri = i['player']['matchHistoryUri']
    print(part_id)


    # timestamp 날짜로 변환
    #datetime = datetime.datetime.fromtimestamp(1578515048756 / 1000)
