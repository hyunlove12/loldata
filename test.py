import datetime

if __name__ == '__main__':
    # timestamp 날짜로 변환
    datetime = datetime.datetime.fromtimestamp(60017 / 1000)
    print(datetime)