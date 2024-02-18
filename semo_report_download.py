import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    setup_and_download_reports(current_directory)
    merge_data(current_directory)

def setup_and_download_reports(current_directory):
    """Sets up directories and downloads reports based on a CSV file."""
    downloads_main_dir = create_main_download_directory(current_directory)
    download_dir = create_versioned_download_directory(downloads_main_dir)
    csv_file = os.path.join(current_directory, 'report_list.csv')
    download_reports(download_dir, csv_file)

def merge_data(current_directory):
    """Merges CSV files from download directories and saves them into an output directory."""
    base_dir = os.path.join(current_directory, 'Downloads')
    output_dir = os.path.join(current_directory, 'Output_Data')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data_folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder)) and 'Downloaded_Data_' in folder]
    data_folders += [output_dir]  # Include Output_Data for merging

    merged_dataframes = {}

    for folder_name in data_folders:
        folder_path = os.path.join(base_dir, folder_name) if folder_name != os.path.basename(output_dir) else output_dir
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            new_df = pd.read_csv(file_path)

            if file_name in merged_dataframes:
                merged_dataframes[file_name] = pd.concat([merged_dataframes[file_name], new_df], ignore_index=True)
            else:
                merged_dataframes[file_name] = new_df

    for file_name, df in merged_dataframes.items():
        df = df.drop_duplicates()
        sort_column = 'StartTime' if 'StartTime' in df.columns else 'TradeDate' if 'TradeDate' in df.columns else None
        if sort_column:
            df = df.sort_values(by=sort_column)

        df.to_csv(os.path.join(output_dir, file_name), index=False)

    print(f'Merged files are saved in {output_dir}.')

def create_main_download_directory(current_directory):
    """Creates a main download directory."""
    downloads_main_dir = os.path.join(current_directory, "Downloads")
    if not os.path.exists(downloads_main_dir):
        os.makedirs(downloads_main_dir)
    return downloads_main_dir

def create_versioned_download_directory(downloads_main_dir):
    """Creates a versioned download directory within the main download directory with date and version."""
    today = datetime.now()
    date_str = today.strftime("%d_%m_%Y")
    dir_number = 1
    while True:
        dir_name = f"Downloaded_Data_{date_str}_{dir_number}"
        download_dir = os.path.join(downloads_main_dir, dir_name)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            return download_dir
        dir_number += 1

def download_reports(download_dir, csv_file):
    """Downloads reports based on a given CSV file."""
    dataframe = pd.read_csv(csv_file, dtype={'report_id': str})
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": False,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    reports_downloaded = 0

    for index, row in dataframe.iterrows():
        report_id = row['report_id']
        report_name = row['name']
        chart_required = row['chart?'].lower() == 'y'
        url = f"https://www.sem-o.com/market-data/dynamic-reports/#BM-{report_id}"
        driver.get(url)

        try:
            if chart_required:
                wait_and_click(driver, By.ID, "dynamic-reports-table")
            wait_and_click(driver, By.CSS_SELECTOR, ".icon.icon-download")
            print(f"Downloaded report ID: {report_id} - {report_name}.")
            reports_downloaded += 1
        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f"Failed to interact with the elements for report ID {report_id} - {report_name}. Reason: {e}")
            continue
        time.sleep(0.5)

    print(f"Successfully downloaded {reports_downloaded}/{len(dataframe)} reports.")
    driver.quit()

def wait_and_click(driver, by_method, selector):
    """Waits for an element to be clickable and then clicks it."""
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by_method, selector)))
        element.click()
    except ElementClickInterceptedException as e:
        driver.execute_script("arguments[0].click();", element)

if __name__ == "__main__":
    main()
