import requests
import datetime
import sys
import json

sys.path.append('./data/key_config.json')
import config

if __name__ == '__main__':
    # git ignore하면 추적 자체를 하지 않는다...
    # 아이디에 대한 기본 정보 가져오기
    f = open('./data/key_config.json', 'r')
    js = json.loads(f.read())
    api_key = js['apiKey']
    #hd = js['headers']
    nick_name = "봉익천상"
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
    print(res.json())
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
    match_list = []
    # dict -> key기준 반복
    # gameId 저장
    for i, r in enumerate(result['matches']):
        match_list.append(r['gameId'])
    #print(res.json()['endIndex'])
    #print(res.json()['startIndex'])
    #print(result['totalGames'])
    #print(result['matches'][0]['gameId'])
    #print(result['matches'][0]['role'])
    #print(result['matches'][0]['season'])
    match_id = result['matches'][0]['gameId']

    # match별 게임 정보
    #url = 'https://kr.api.riotgames.com/lol/match/v4/matches/{}'.format(match_id)
    #res = requests.get(url=url, headers=headers)
    #print(res.json())
    #match_result = res.json()
    match_part_id = []

    # 'platformId': 'KR', 'gameId': 4060252070, 'champion': 63, 'queue': 420, 'season': 13, 'timestamp': 1577901783254, 'role': 'DUO_SUPPORT', 'lane': 'BOTTOM'
    # timeline 별 게임정보 -> gameId 별로 데이터 저장
    for r in match_list:
        # 게임 속 participationId 가져오기
        url = 'https://kr.api.riotgames.com/lol/match/v4/matches/{}'.format(r)
        res = requests.get(url=url, headers=headers)
        match_result = res.json()
        #print(match_result)
        # 반복문 돌려서 해당 플레이어의  id 가져오기
        for i in match_result['participantIdentities']:
            if i['player']['summonerName'] == '봉익천상':
                part_id = i['participantId']
                matchHistoryUri = i['player']['matchHistoryUri']
        #print(part_id)

        url = 'https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{}'.format(r)
        res = requests.get(url=url, headers=headers)
        print(res.json())
        timeline_match_result = res.json()
        events_list = []
        print('gameId', r)
        # frames안에 list객체가 timestamp단위로 데이터 들어가 있음
        for i, r in enumerate(timeline_match_result['frames']):
            # timestamp기준 -> participantFrames, events객체
            # participantFrames -> 1 ~ 10까지의 map객체 -> 해당 유저의 participantId를 찾아서 몇번 객체인지 찾아야 한다
            timestamp = r['timestamp']
            print('timestamp', timestamp)
            # key : 1 ~ 10, value : 해당 유저에 대한 종합 정보
            for key, value in r['participantFrames'].items():
                # 해당 유저의 participantId가 part_id와 같은 경우
                part_frames = value['participantId'] if value['participantId'] == part_id else ''
                print("11", part_frames)
            # events 리스트에서 해당 유저와 관련 된 데이터만 추출 -> killerId or victimId
            # get으로 값 추출 시 없는 값이면 none반환 -> ['']로 추출하면 에러 발생
            # 해당 시간에 유저가 관련된 event가 있으면 저장
            for ind, res in enumerate(r['events']):
                if res.get('killerId') == part_id:
                    events_list.append(res)
                    continue
                elif res.get('victimId') == part_id:
                    events_list.append(res)
                    continue
            print(events_list)
    # timestamp 날짜로 변환60017
    #datetime = datetime.datetime.fromtimestamp(1578515048756 / 1000)
