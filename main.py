from addFriends import addFriends
from wallPost import wallPost
from time import sleep
from datetime import datetime

def main():
    print('Начало работы')
    phone = '+79012993071'
    password = 'qwerASDF1234'
    while True:
        date = datetime.now()
        time = str(date)[11:]
        if time[:2] in ['11', '14']:
            wallPost(1, phone, password)
            addFriends(phone, password)
            with open('отчет.txt', 'a', encoding='utf-8') as f:
                print(date, file=f)
        sleep(3600)


if __name__ == '__main__':
    main()