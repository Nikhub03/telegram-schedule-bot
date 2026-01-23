import time
import signal
import sys
from schedule import bot  # Импорт Token

def signal_handler(sig, frame):
    print("\nБот остановлен.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("Бот онлайн!")

while True:
    try:
        bot.infinity_polling(none_stop=True, timeout=10)
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
        break
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(15)
