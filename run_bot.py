import subprocess

if __name__ == "__main__":
    subprocess.Popen(["python", "bot/barbarzyncy_bot.py"])
    subprocess.Popen(["python", "bot/utils/update_bot.py"])
    subprocess.Popen(["python", "bot/utils/check_bot_health.py"])