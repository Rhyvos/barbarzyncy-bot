import subprocess
import os
import argparse


def start_bot():
    subprocess.Popen(["python", "BarbarzyncyBot/bot/barbarzyncy_bot.py"], preexec_fn=os.setsid)
    subprocess.Popen(["python", "BarbarzyncyBot/bot/utils/update_bot.py"], preexec_fn=os.setsid)
    subprocess.Popen(["python", "BarbarzyncyBot/bot/utils/check_bot_health.py"], preexec_fn=os.setsid)

def kill_bot():
    subprocess.Popen(["pkill", "-f", "barbarzyncy_bot.py"])
    subprocess.Popen(["pkill", "-f", "update_bot.py"])
    subprocess.Popen(["pkill", "-f", "check_bot_health.py"])



def main():
    parser = argparse.ArgumentParser(description='Uruchamia bota, lub kończy jego działanie.')
    parser.add_argument('--kill', action='store_true', help='Ubija wszystkie procesy związane z botem')
    args = parser.parse_args()

    if args.kill:
        kill_bot()
    else:
        start_bot()

if __name__ == "__main__":
    main()