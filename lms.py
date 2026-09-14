from playwright.sync_api import sync_playwright
import os
import sys
import time
from pathlib import Path

if getattr(sys, "frozen", False):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(
        Path(sys._MEIPASS) / "ms-playwright"
    )

import time
chapt = ["Bài giảng 1: Công tác sinh viên",
         "Bài giảng 2: Quy định đào tạo tín chỉ",
         "Bài giảng 3: Quy định Khảo thí và Đảm bảo chất lượng giáo dục",
         "Bài giảng 4: Quy định sử dụng thư viện",
         "Nội dung 1 (trực tiếp sáng thứ Ba ngày 25/8/2026)",
         "Nội dung 2 (trực tiếp chiều thứ Ba ngày 25/8/2026)",
         "Nội dung 3 (trực tiếp sáng thứ Tư ngày 26/8/2026)",
         "Nội dung 4 (trực tiếp chiều thứ Tư ngày 26/8/2026)",
         "Nội dung 5 (trực tiếp sáng thứ Năm ngày 27/8/2026)",
         "Nội dung 6 (trực tiếp chiều thứ Năm ngày 27/8/2026)"]

         #these are special ones, the lectures have the same name, so i can only use get_by_role("button", name="{name}")
         #"Chuyên đề 3: Công tác sinh viên và kỹ năng quản lý tài chính cá nhân",
         #"Chuyên đề 4: Học tập trong kỷ nguyên số và AI",
         #"Chuyên đề 5: Nghiên cứu khoa học, đổi mới sáng tạo và khởi nghiệp",
         #"Chuyên đề 6: Hoạt động Đoàn, câu lạc bộ và phát triển sinh viên",
         #"Chuyên đề 7: Pháp luật, an ninh và an toàn cho sinh viên",
         #"Chuyên đề 8: Giáo dục chính trị, tư tưởng và trách nhiệm công dân"]

playback_speed = [0.75, 1, 1.25, 1.5, 1.75, 2, 4]
speed = 6 #SET SPEED OF VIDEO


with sync_playwright() as playwright:
    #remembers the user's session, but they have to log in first
    browser = playwright.chromium.launch_persistent_context("cookie",headless=False)
    page=browser.new_page()

    #PUT THE IRL OF THE FIRST VIDEO HERE
    page.goto("https://lms.ptit.edu.vn/courses/course-v1:PTIT+TLCD+20261/join?lessonId=block-v1%3APTIT%2BTLCD%2B20261%2Btype%40vertical%2Bblock%4040e3f65ae9494c628e5bb6a46a80c157")

    #autocomplete
    for i in range(len(chapt)):
        if i <= 9:
            element = page.get_by_title(chapt[i])
            if i != 0:
                print("clicking",chapt[i])
                element.click()
                #time.sleep(0.5)
            lecture_block = element.locator("../../../../../..").locator(":scope > *").nth(1) #parent block is 6 indents above, get the container with the lectures
            lectures = lecture_block.locator(":scope > * > * > *") #should point towards every single lecture (if im not totally braindead)
            print(lectures.count())

            for lec in range(lectures.count()):
                lectures.nth(lec).locator(":scope > *").nth(1).locator(":scope > * > * > *").nth(0).click() #enter the lecture
                check = lectures.nth(lec).locator(":scope > *").nth(0).locator(":scope > *")
                if "ant-checkbox-wrapper-checked" in check.get_attribute("class").split():
                    continue
                else:
                    play_btn = page.locator("button.plyr__control--overlaid")
                    settings = play_btn.locator("..").locator(":scope > *").nth(0).locator(":scope > *").nth(6).locator(":scope > *").nth(0)
                    speed_menu = settings.locator("..").locator(":scope > *").nth(1).locator(":scope > * > *").nth(0).locator(":scope > * > *").nth(2)

                    settings.click()
                    speed_menu.click()
                    page.locator(f'button.plyr__control[data-plyr="speed"][value="{playback_speed[speed]}"]').click()
                    
                    play_btn.click()

                    while True:
                        try:
                            check.get_attribute("class").split()
                        except Exception:
                            break

        else:
            pass

    while True:
        pass