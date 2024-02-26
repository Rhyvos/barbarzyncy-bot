import schedule
import subprocess
import time
import psutil
import os
import signal
import socket

from bot_logger import bot_logger

logger = bot_logger("check_bot_health")

def check():
    logger.info("Checking bot health...")
    server_address = ('localhost', 12345)
    message = "ping"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(5)
            s.connect(server_address)
            s.sendall(message.encode())
            data = s.recv(1024)
            logger.info(f"Received response: {data.decode()}")
        except socket.timeout:
            logger.info("Timeout - Unable to receive response from the server.")
            reset()
        except Exception as e:
            logger.info(f"Error: {e}")
            reset()

def reset():
    logger.info("Resetting bot...")
    target_script = "bot/barbarzyncy_bot.py"

    bot_process_exists = False

    try:
        bot_process_exists = any(
            'python' in process.info['cmdline'] and target_script in process.info['cmdline']
            for process in psutil.process_iter(attrs=['pid', 'cmdline'])
        )
    except Exception as e:
            logger.info(f"Error: {e}")

    if bot_process_exists:
        logger.info(f"Found the {target_script} process. Closing...")
        try:
            for process in psutil.process_iter(attrs=['pid', 'cmdline']):
                if 'python' in process.info['cmdline'] and target_script in process.info['cmdline']:
                    os.kill(process.info['pid'], signal.SIGKILL)
                    logger.info(f"Closed the {target_script} process (PID: {process.info['pid']}).")
                    break
        except Exception as e:
            logger.info(f"Error closing the {target_script} process: {e}")

 
    logger.info(f"Restarting {target_script}...")
    subprocess.Popen(["python", target_script])




if __name__ == "__main__":
    schedule.every(1).seconds.do(check)
    while True:
        schedule.run_pending()
        time.sleep(1)