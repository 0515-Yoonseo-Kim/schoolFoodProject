import os
import asyncio
from playwright.async_api import async_playwright

async def download_image(page, image_url, save_folder, file_name):
    try:
        # 이미지 다운로드
        response = await page.request.get(image_url)
        if response.status == 200:
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as file:
                file.write(await response.body())
            print(f"Image saved to {file_path}")
        else:
            print(f"Failed to download image from {image_url}. Status code: {response.status}")
    except Exception as e:
        print(f"Failed to download image from {image_url}. Error: {e}")

async def extract_and_download_images(playwright):
    # 브라우저 실행 및 창 열기
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # 특정 링크로 이동함
    await page.goto("https://shinjeong.sen.hs.kr/51743/subMenu.do")

    # 페이지 로드 대기
    await page.wait_for_load_state('load')

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
                        
                        # 클릭 후 팝업이 뜨는 것을 기다림
                        await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='visible')

                        # 이미지 요소 찾기
                        img_element = await page.query_selector('div.layer_popup#divLayerMlsvPopup img')
                        if img_element:
                            img_src = await img_element.get_attribute('src')
                            img_url = f"https://shinjeong.sen.hs.kr{img_src}"
                            print(f"Found image: {img_url}")

                            # 파일 이름 생성
                            file_id = onclick_attribute.split("'")[1]  # 작은 따옴표로 분리하여 ID 추출
                            file_name = f"{file_id}.jpg"

                            # 이미지 다운로드
                            await download_image(page, img_url, 'downloaded_images', file_name)

                        # 팝업 닫기
                        close_button = await page.query_selector('button[onclick="fnLayerPopupClose();"]')
                        if close_button:
                            await close_button.click()
                            await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='hidden')
                        else:
                            print("No close button found, manually navigating back.")
                            await page.go_back()
                        await page.wait_for_load_state('load')
    else:
        print("Calendar Div not found")

    # 브라우저 종료
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await extract_and_download_images(playwright)

asyncio.run(main())
import os
import asyncio
from playwright.async_api import async_playwright

async def download_image(page, image_url, save_folder, file_name):
    try:
        # 이미지 다운로드
        response = await page.request.get(image_url)
        if response.status == 200:
            os.makedirs(save_folder, exist_ok=True)
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as file:
                file.write(await response.body())
            print(f"Image saved to {file_path}")
        else:
            print(f"Failed to download image from {image_url}. Status code: {response.status}")
    except Exception as e:
        print(f"Failed to download image from {image_url}. Error: {e}")

async def extract_and_download_images(playwright):
    # 브라우저 실행 및 창 열기
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    # 특정 링크로 이동함
    await page.goto("https://shinjeong.sen.hs.kr/51743/subMenu.do")

    # 페이지 로드 대기
    await page.wait_for_load_state('load')

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
                        
                        # 클릭 후 팝업이 뜨는 것을 기다림
                        await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='visible')

                        # 이미지 요소 찾기
                        img_element = await page.query_selector('div.layer_popup#divLayerMlsvPopup img')
                        if img_element:
                            img_src = await img_element.get_attribute('src')
                            img_url = f"https://shinjeong.sen.hs.kr{img_src}"
                            print(f"Found image: {img_url}")

                            # 파일 이름 생성
                            file_id = onclick_attribute.split("'")[1]  # 작은 따옴표로 분리하여 ID 추출
                            file_name = f"{file_id}.jpg"

                            # 이미지 다운로드
                            await download_image(page, img_url, 'downloaded_images', file_name)

                        # 팝업 닫기
                        close_button = await page.query_selector('button[onclick="fnLayerPopupClose();"]')
                        if close_button:
                            await close_button.click()
                            await page.wait_for_selector('div.layer_popup#divLayerMlsvPopup', state='hidden')
                        else:
                            print("No close button found, manually navigating back.")
                            await page.go_back()
                        await page.wait_for_load_state('load')
    else:
        print("Calendar Div not found")

    # 브라우저 종료
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await extract_and_download_images(playwright)



if __name__=="__main__":
    asyncio.run(main())