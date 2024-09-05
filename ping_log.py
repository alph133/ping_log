import subprocess
import time
from datetime import datetime

# 紀錄失敗變成功的次數
success_count = 0
last_ping_failed = False  # 用來追蹤上次的 ping 是否失敗
fail_time = None  # 記錄失敗時的時間

def log_to_file(message):
    # 將訊息寫入 txt 檔案，附加模式 'a' 會在檔案末尾追加內容
    with open('ping_log.txt', 'a') as file:
        file.write(message + '\n')

def ping_website(url):
    global success_count, last_ping_failed, fail_time
    # Windows 下使用 '-n 1' 發送一次 ICMP 請求
    command = ['ping', '-n', '1', url]
    
    try:
        # 開始 ping
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        current_time = datetime.now()  # 獲取當前時間
        
        # 檢查返回碼，0 表示成功，其他則表示失敗
        if output.returncode != 0:
            if not last_ping_failed:  # 第一次檢測到失敗時記錄
                fail_time = current_time  # 記錄失敗時間
                message = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Ping {url} failed"
                log_to_file(message)
            raise Exception("Ping failed")

        else:
            print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Ping {url} successful")
            
            # 如果上次 ping 失敗，這次成功了，記錄成功並增加次數
            if last_ping_failed:
                success_count += 1
                recovery_time = current_time - fail_time  # 計算從失敗到恢復的時間差
                message = (f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Ping {url} recovered successfully! "
                           f"Total recoveries: {success_count}   Downtime = {recovery_time}" + '\n')
                print(message)
                log_to_file(message)  # 將成功訊息寫入檔案
                last_ping_failed = False  # 將狀態重置為成功
    except Exception as e:
        current_time = datetime.now()  # 獲取當前時間
        print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Ping {url} failed: {str(e)}")
        last_ping_failed = True  # 設置狀態為失敗

if __name__ == "__main__":
    url = "www.google.com"  # 指定需要 ping 的網址
    while True:
        ping_website(url)
        time.sleep(5)  # 每隔 5 秒重新 ping 一次
