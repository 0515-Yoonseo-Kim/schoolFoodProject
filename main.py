import argparse
import asyncio
from Scraper import extract_and_download_images, PageArgs

def main():
    parser = argparse.ArgumentParser(description="Scrape school meal images.")
    parser.add_argument('--school_name', type=str, help='Name of the school to scrape images for')
    parser.add_argument('--main_page', type=str, help='URL of the main page to scrape from')

    args = parser.parse_args()

    # PageArgs 인스턴스를 생성할 때 argparse 인자들을 사용합니다.
    pageargs = PageArgs(
        main_page=args.main_page or PageArgs().main_page,
        school_name=args.school_name or PageArgs().school_name
    )

    asyncio.run(extract_and_download_images(pageargs))

if __name__ == "__main__":
    main()
