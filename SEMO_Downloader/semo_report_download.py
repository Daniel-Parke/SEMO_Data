import asyncio
import httpx
from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd
from asyncio import Semaphore
import os

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppress httpx detailed logs


@dataclass
class ReportURLs:
    report_list_path: str = "report_list_short.csv"
    reports: pd.DataFrame = field(init=False)
    urls: Dict[str, List[str]] = field(default_factory=dict, init=False)
    data: Dict[str, pd.DataFrame] = field(default_factory=dict, init=False)
    semaphore: Semaphore = field(default=Semaphore(50), init=False)

    async def async_init(self):
        logging.info("Initializing ReportURLs class.")
        self.reports = pd.read_csv(self.report_list_path, dtype={'report_id': str})
        await self.generate_all_urls_async()
        await self.fetch_and_merge_data()

    def create_api_url(self, report_num, page="1", page_size="5000"):
        start_time = "2010-11-18T00:00"
        end_time = "2030-02-18T23:59"
        sort_by = "StartTime"
        order_by = "ASC"
        participant_name = ""
        resource_name = ""
        resource_type = ""
        base_url = f"https://reports.sem-o.com/api/v1/dynamic/BM-{report_num}?"

        url = (
            f"{base_url}"
            f"StartTime=%3E%3D{start_time}&"
            f"EndTime=%3C%3D{end_time}&"
            f"sort_by={sort_by}&"
            f"order_by={order_by}&"
            f"ParticipantName={participant_name}&"
            f"ResourceName={resource_name}&"
            f"ResourceType={resource_type}&"
            f"page={page}&"
            f"page_size={page_size}"
        )

        return url

    async def get_total_pages(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response_data = response.json()
            total_pages = response_data['pagination']['totalPages']
            return total_pages

    async def generate_all_urls_async(self):
        logging.info("Asynchronously generating all URLs for reports.")
        self.urls = {}
        tasks = []
        for index, row in self.reports.iterrows():
            report_id = row['report_id']
            report_name = row['name']
            task = asyncio.create_task(self.fetch_total_pages_and_generate_urls(report_id, report_name))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def fetch_total_pages_and_generate_urls(self, report_id, report_name):
        initial_url = self.create_api_url(report_id)
        total_pages = await self.get_total_pages(initial_url)
        report_urls = [self.create_api_url(report_id, page=str(page)) for page in range(1, total_pages + 1)]
        self.urls[report_name] = report_urls
    
    async def fetch_with_retry(self, url, url_index, total_urls, report_name):
        retries = 3
        backoff_factor = 0.5
        async with self.semaphore:
            for attempt in range(1, retries + 1):
                try:
                    async with httpx.AsyncClient(timeout=20.0) as client:
                        response = await client.get(url)
                        response.raise_for_status()
                        logging.info(f"Request {url_index}/{total_urls} completed for {report_name}.")
                        return response.json()
                except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                    logging.warning(f"Timeout on attempt {attempt} for {url}: {e}")
                    if attempt == retries:
                        logging.error(f"Max retries reached for {url}.")
                        return None
                    sleep_duration = backoff_factor * (2 ** (attempt - 1))
                    logging.info(f"Retrying in {sleep_duration} seconds...")
                    await asyncio.sleep(sleep_duration)
                except httpx.RequestError as e:
                    logging.error(f"Request error for {url}: {e}")
                    return None

    async def fetch_and_merge_data(self):
        logging.info("Starting to fetch and merge data for all reports.")
        for report_name, urls in self.urls.items():
            logging.info(f"Processing {len(urls)} URLs for {report_name}.")
            tasks = [self.fetch_with_retry(url, i+1, len(urls), report_name) for i, url in enumerate(urls)]
            pages_data = await asyncio.gather(*tasks)
            combined_data = self.combine_data(pages_data)
            if combined_data:
                df = pd.DataFrame(combined_data)
                self.save_data_to_csv(df, report_name)  # Call save method immediately after data is ready
                logging.info(f"Completed download and merging for {report_name}: {len(combined_data)} items fetched.")
            else:
                logging.warning(f"No data found for {report_name}.")

    def combine_data(self, pages_data):
        all_data = []
        for page_data in pages_data:
            if page_data and 'items' in page_data:
                all_data.extend(page_data['items'])
        return all_data

    def save_data_to_csv(self, df, report_name):
        output_dir = "Output_Data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = os.path.join(output_dir, f"{report_name}.csv")
        df.to_csv(file_path, index=False)
        logging.info(f"Saved {report_name} data to {file_path}.")