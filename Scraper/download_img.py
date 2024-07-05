# Scraper/download_img.py
import os

async def download_image(page, img_url, download_folder, file_name):
    os.makedirs(download_folder, exist_ok=True)
    img_path = os.path.join(download_folder, file_name)
    
    # Check if the image already exists
    if not os.path.exists(img_path):
        async with page.expect_download() as download_info:
            await page.evaluate(f"fetch('{img_url}').then(res => res.blob()).then(blob => {{ const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = '{file_name}'; document.body.appendChild(a); a.click(); document.body.removeChild(a); }});")
        download = await download_info.value
        await download.save_as(img_path)
        print(f"Downloaded image to {img_path}")
    else:
        print(f"Image already exists at {img_path}, skipping download.")