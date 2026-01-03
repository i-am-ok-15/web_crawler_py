import asyncio
import aiohttp
from urllib.parse import urlparse
from crawl import normalize_url, extract_page_data, get_url_links_from_html

class AsyncCrawler:

    def __init__(self, base_url, max_concurrency, max_pages):
        
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    

    async def add_page_visit(self, normalized_url):
        if self.should_stop == True:
            return False
        
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print(f"Reached maximum number of pages to crawl -> {self.max_pages}.")
                return False
            self.page_data[normalized_url] = None
            return True
        

    async def get_html(self, url):
        
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:

            if response.status >= 400:
                print(f"Error: Client Error Response -> {response.status}")
                return None
            
            content_type = response.headers.get("Content-Type", "")
            content_type_cleaned = content_type.split(";")[0].strip()

            if content_type_cleaned != "text/html":
                return None
            
            try:
                html = await response.text()
            except Exception as e:
                print(e)
            
            return html


    async def crawl_page(self, current_url):

        if self.should_stop == True:
            return

        if urlparse(current_url).netloc != self.base_domain:
            return     
        
        normalized_url = normalize_url(current_url)

        visited = await self.add_page_visit(normalized_url)

        if visited == False:
            return

        async with self.semaphore:

            print(f"Getting Page Data From -> {normalized_url}")

            try:
                data = await self.get_html(current_url)
            except Exception as e:
                print(e)
                return
            
            if data is None:
                async with self.lock:
                    del self.page_data[normalized_url]
                return

            rich_data = extract_page_data(data, current_url)

            async with self.lock:
                self.page_data[normalized_url] = rich_data

            urls = get_url_links_from_html(data, self.base_url)
            tasks = []

            for url in urls:
                try:
                    data = asyncio.create_task(self.crawl_page(url))
                    self.all_tasks.add(data)
                    tasks.append(data)
                except Exception as e:
                    print(e)
                    continue

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        self.page_data = {
            url: data for url, data in self.page_data.items() if data is not None
        }
        return self.page_data
    
async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency=max_concurrency, max_pages=max_pages) as crawler:
        return await crawler.crawl()
    

