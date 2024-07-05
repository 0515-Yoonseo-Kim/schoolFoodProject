import asyncio
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from dataclasses import dataclass, field
from .download_img import download_image

@dataclass
class PageArgs:
    main_page: str = field(
        default="https://moonyoung.sen.hs.kr/59366/subMenu.do",
        metadata={"description": "급식 이미지를 스크래핑 할 링크를 입력해주세요."}
    )
    school_name: str = field(
        default="서울문영여고",
        metadata={"description": "스크래핑을 진행할 학교 이름을 입력해주세요."}
    )
    
async def scrape_menu_data(page, pageargs, menu_list):
    try:
        # 클릭 후 팝업이 뜨는 것을 기다림
        await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='visible')
        
        # 이미지 요소 찾기
        img_element = await page.query_selector('div.layer_popup#divLayerMlsvPopup img')
        if img_element:
            img_src = await img_element.get_attribute('src')
            img_url = f"https://moonyoung.sen.hs.kr{img_src}"
            print(f"Found image: {img_url}")

            # 등록일 요소 찾기
            date_element = await page.query_selector('tr:has(th:text-is("등록일")) td.ta_l')
            meal_element = await page.query_selector('tr:has(th:text-is("급식")) td.ta_l')
            menu_element = await page.query_selector('tr:has(th:text-is("식단")) td.ta_l')

            if date_element and meal_element and menu_element:
                date_text = await date_element.text_content()
                meal_text = await meal_element.text_content()
                menu_text = await menu_element.text_content()
                menu_text = menu_text.lstrip()

                date_part, day_part = date_text.strip().split(' ', 1)
                meal_part = meal_text.strip()
                file_name = f"{date_part}_{day_part}_{meal_part}.jpg"
                file_name = file_name.replace(" ", "_")

                await download_image(page, img_url, pageargs.school_name, file_name)

                menu_list.append({
                    "Date": ' '.join([date_part, day_part]),
                    "Meal": meal_part,
                    "Menu": menu_text,
                    "Image URL": img_url,
                    "File Name": file_name
                })
        
        # 팝업 닫기
        close_button = await page.query_selector('button[onclick="fnLayerPopupClose();"]')
        if close_button:
            await close_button.click()
            await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='hidden')
        else:
            print("No close button found, manually navigating back.")
            await page.go_back()
        await page.wait_for_load_state('load')
    except PlaywrightTimeoutError:
        print("Timeout waiting for the popup to become visible. Skipping to next item.")

async def select_days(page, pageargs, menu_list):
    while True:
        # 페이지의 연월 정보를 출력
        year_element = await page.query_selector('select[name="srhMlsvYear"] > option[selected]')
        month_element = await page.query_selector('select[name="srhMlsvMonth"] > option[selected]')
        year = await year_element.text_content() if year_element else "Unknown"
        month = await month_element.text_content() if month_element else "Unknown"
        print(f"Scraping data for {year}-{month}")

        # <div class="calendar_schedule monthly"> 요소 찾기
        calendar_div = await page.query_selector('div.calendar_schedule.monthly')
        if calendar_div:
            # <tbody> 요소 찾기
            tbody = await calendar_div.query_selector('tbody')
            if tbody:
                # <tbody>의 <tr> 요소들 찾기
                rows = await tbody.query_selector_all('tr')
                for row in rows:
                    # 각 <tr> 요소의 <td> 요소들 찾기
                    cells = await row.query_selector_all('td')
                    for cell in cells:
                        # <a> 요소 찾기
                        link = await cell.query_selector('a[onclick]')
                        if link:
                            print("Found <a> tag with onclick event:")
                            onclick_attribute = await link.get_attribute('onclick')
                            print(onclick_attribute)

                            # <a> 요소 클릭
                            await link.click()
                            await scrape_menu_data(page, pageargs, menu_list)

        # 이전 달 버튼 클릭
        if year == "2017년" and month == "1월":
            print("Reached January 2017, stopping the script.")
            break
        prev_button = await page.query_selector('a.cal_prev')
        if prev_button:
            await prev_button.click()
            await page.wait_for_load_state('load')

async def extract_and_download_images(pageargs: PageArgs):
    menu_list = []
    
    async with async_playwright() as playwright:
        # 브라우저 실행 및 창 열기
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 특정 링크로 이동함
        await page.goto(pageargs.main_page)

        # 페이지 로드 대기
        await page.wait_for_load_state('load')

        # 연월 선택 및 데이터 스크래핑
        await select_days(page, pageargs, menu_list)

        # 브라우저 종료
        await browser.close()
        
    # 급식 메뉴 리스트를 데이터프레임으로 변환
    df = pd.DataFrame(menu_list)
    
    # 데이터프레임을 CSV 파일로 저장
    df.to_csv(f"{pageargs.school_name}_menu.csv", index=False)
    print("Saved menu data to CSV file.")
