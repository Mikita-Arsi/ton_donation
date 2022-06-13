import requests
import time as t
import pyttsx3 as p3
from playsound import playsound
from config import wallet, sound_name


class Event:
    def __init__(self):
        self.result = requests.get(f'https://api.ton.sh/getTransactions?address={wallet}').json()['result'][0]
        self.message = self.message_filter(self.result['received']['message'])

    def message_filter(self, message: str):
        if len(message) == 33 and ' ' not in message:
            return ' '
        return message

    def play_donate(self):
        playsound(sound_name)
        print(self.message + '\n')
        t.sleep(0.8)
        engine.say(f"Вы получили {str(self.result['received']['nanoton'] * 0.000000001)}тон")
        t.sleep(0.2)
        engine.say(self.message)
        engine.runAndWait()


def voice_config():
    global engine

    engine = p3.init()
    engine.setProperty('voice', 'ru')
    engine.setProperty('rate', 150)


def main(last_hash: str):
    print(t.strftime("%H:%M:%S", t.localtime()), last_hash, '\n')
    voice_config()

    while True:
        try:
            t.sleep(2.011)
            event = Event()
            if event.result['hash'] == last_hash and event.result['received']['from'] != 'external':
                print(t.strftime("%H:%M:%S", t.localtime()), event.result['received']['nanoton'] * 0.000000001,
                      event.result['hash'])
                event.play_donate()
                last_hash = event.result['hash']
            del event
        except UnicodeDecodeError:
            print("Неправильно указан аудиофайл")
            exit()

        except Exception as e:
            continue


if __name__ == "__main__":
    try:
        main(requests.get(f'https://api.ton.sh/getTransactions?address={wallet}').json()['result'][0]['hash'])
    except KeyError:
        print("Неправильно указан кошелёк")
        exit()
