from addFriends import addFriends
from wallPost import wallPost
from time import sleep
from datetime import datetime

def main():
    print('Начало работы')
    while True:
        date = datetime.now()
        time = str(date)[11:]
        if time[:2] in ['11', '13']:
            wallPost(1)
            addFriends()
        sleep(3600)


if __name__ == '__main__':
    main()
