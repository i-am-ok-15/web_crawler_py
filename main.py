import sys
import asyncio
from async_crawler import crawl_site_async
from csv_report import write_csv_report

def get_url():
    if len(sys.argv) == 4:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")
    elif len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    return base_url


async def main():
    base_url = get_url()
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])

    try:
        crawl_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    except Exception as e:
        print(e)
        return
    
    page_count = 0
    for page in crawl_data.values():
        if page is None:
            continue
        page_count += 1
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")

    print(f"{page_count} pages crawled in total. Crawl complete.")
    write_csv_report(crawl_data)

    
if __name__ == "__main__":
    asyncio.run(main())
