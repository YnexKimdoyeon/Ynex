import os
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class Macro:
    def __init__(self,ins):
        self.ins = ins
    def login(self):
        self.ins.Print_Result.emit("[*] 클라우드 플레어 우회를 진행한뒤 값을 설정후 실행해주세요.")
        os.system("taskkill /f /im Chrome.exe /t")
        subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223')  # -- Admin Path
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.get("https://119db.com")
        s

    def Play_login(self, username, password):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get("https://119db.com/bbs/logout.php")
        time.sleep(3)
        self.driver.get("https://119db.com/bbs/login.php")
        self.driver.execute_script(f'document.getElementById("login_id").value = "{username}";')
        self.driver.execute_script(f'document.getElementById("login_pw").value = "{password}";')
        self.driver.find_element(By.CSS_SELECTOR,'button.btn.btn-color.pull-right').click()
        self.NickName = self.driver.find_element(By.CSS_SELECTOR,'h3').text.rstrip()
        time.sleep(2)

    def Main_Controller(self,Start_PG,End_PG,Delay1,Delay2,username,password):
        self.ins.Print_Result.emit(f"[시작페이지] : {Start_PG}")
        self.ins.Print_Result.emit(f"[종료페이지] : {End_PG}")
        self.ins.Print_Result.emit(f"[딜레이_1] : {Delay1}")
        self.ins.Print_Result.emit(f"[딜레이_2] : {Delay2}")
        self.ins.Print_Result.emit(f"[아이디] : {username}")
        self.ins.Print_Result.emit(f"[비밀번호] : {password}")
        self.Play_login(username,password)
        if End_PG <= Start_PG:
            for Page in range(Start_PG,End_PG-1,-1):
                self.driver.get(f'https://119db.com/board_free_new/p{Page}')
                Board_List = [i.get_attribute('href') for i in self.driver.find_elements(By.CSS_SELECTOR,'div.wr-subject > a')]
                Board_List.reverse()
                for Board_Link in Board_List:
                    try:
                        self.driver.get(Board_Link)
                        # Com_Div = self.driver.find_element(By.ID,'viewcomment')
                        # User_List = [i.text.rstrip() for i in Com_Div.find_elements(By.CSS_SELECTOR,'span.member')]
                        # if self.NickName not in User_List:
                        #     Select_Comment = self.Read_Content()
                        #     if Select_Comment != False:
                        self.driver.find_element(By.CSS_SELECTOR,'span.view-good > a').click()
                        # self.driver.find_elements(By.ID, "wr_content")[-1].send_keys(Select_Comment)
                        # self.driver.find_element(By.ID, "btn_submit").click()
                        Delay = random.uniform(Delay1,Delay2)
                        # self.Write_Link(self.driver.current_url)
                        # self.ins.Print_Result.emit(f"[구동성공] : 댓글 : {Select_Comment}")
                        self.ins.Print_Result.emit(f"[구동성공] : 딜레이 : {Delay}")
                        time.sleep(Delay)
                    except:
                        self.ins.Print_Result.emit(f"[구동실패] : 예기치 못한 오류")
            self.ins.Print_Result.emit(f"[*] : 프로그램 구동이 완료되었습니다.")
        else:
            self.ins.Print_Result.emit(f"[*] : 종료페이지 값이 시작페이지 값보다 클수 없습니다.")

    def Read_Content(self):
        Comment_List = [i.text.replace("\n","") for i in self.driver.find_elements(By.CSS_SELECTOR,'div.media-content')]
        Last_Comment_List = []

        for Comment in Comment_List:
            if "Congratulation" not in Comment:
                if "수정된" not in Comment:
                    if len(Comment) <= 7:
                        Last_Comment_List.append(Comment)
        if len(Last_Comment_List) != 0:
            del Last_Comment_List[-20:]
            return random.choice(Last_Comment_List)
        return False
    def Write_Link(self,Link):
        with open ("댓글내역.txt",'a',encoding="UTF-8") as File:
            File.write(Link+"\n")