# Scraper/download_img.py
import os

async def download_image(page, img_url, download_folder, file_name):
    os.makedirs(download_folder, exist_ok=True)
    img_path = os.path.join(download_folder, file_name)
    async with page.expect_download() as download_info:
        await page.evaluate(f"fetch('{img_url}').then(res => res.blob()).then(blob => {{ const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = '{file_name}'; document.body.appendChild(a); a.click(); document.body.removeChild(a); }});")
    download = await download_info.value
    await download.save_as(img_path)
    print(f"Downloaded image to {img_path}")
