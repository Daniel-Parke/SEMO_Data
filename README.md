# SEMO Report Downloader and Historical Merger

This Python script automates the process of downloading SEMO reports and merging them with the range of data available through the SEMO API. This script will download all reports as specified in the `report_list.csv` file, merges where applicable, and then saves the downloaded files to the `Output_Data` folder.

There are three scripts to choose from, short, long or full. There are several reports that consist of over 500,000 rows of data so I seperated the reports into short and long types. If you would like to download them all at once, then select the script with `full.py` at the end.

The date range is set to download all data available from 2010 until 2030, so unless the server API changes this should download all available data offered by SEMO on the frontend. I have included the data that is downloaded if the `_short.py` were to be run, the other datasets were unfortunately too large for github with LFS.

# **How to run:**
- Ensure that either `report_list_xxxx.csv` are located in the SEMO_Downloader folder.
- Run the `semo_report_xxxx.py` script on the terminal, or run the first cell located in the .ipynb notebook to run the program. 
- Enjoy your new collection of merged data without the hassle of navigating the website.

- (OPTIONAL) Remove or add rows to the `report_list_xxxxx.csv` if you need to change the report data being downloaded, otherwise just run the script you need and you should be good to go!
<br>

## Script Operation Description:
To run the script simply run the `.py` files, or alternatively run the required cell within the jupyer notebook `.ipynb` file. Here each of the scripts is available to run in a seperate cell if this is more familiar for you.

Once run the script will generate a class object which compiles a list of all the URLs to be accessed, and then begins asynchronously accessing these. Once a particularly report has been fully downloaded and merged, a .csv file will be produced and saved in the `Output_Data` folder.

Currently the program will download and overwrite any existing files that exist with the same name in the `Output_Data` folder. This shouldn't be an issue as the downloader will try to access the full range of data available anyway. If this is an issue though please let me know and I may update the logic. Alternatively if you rename the `Output_Data` folder to something else before running the script again, this will prevent the issue.
<br>

## Features

- **Asynchronous Data Fetching**: Leverages asyncio for concurrent downloading, making the process faster and more efficient.
- **Enhanced Error Handling**: Implements retries and backoff strategies to manage request timeouts or failures gracefully.
- **Automatic URL Generation**: Constructs API URLs dynamically to fetch report data, handling pagination seamlessly from provided `report_list.csv` files.
- **Data Merging**: Combines downloaded data with existing datasets, ensuring chronological order and removing duplicates.


## Functions Overview

### `async_init()`
Initializes the downloading process by loading the report list and preparing URLs for asynchronous fetching. This method replaces the manual setup and selenium navigation, streamlining the download process.

- **Load Report List**: Reads `report_list_short.csv` to prepare a list of reports for download.
- **Generate URLs**: Dynamically constructs URLs for each report, handling pagination through asynchronous requests.

### `create_api_url(report_num, page="1", page_size="5000")`
Generates the URL for a specific report and page, accommodating the SEMO API's requirements for fetching report data.

- **Parameters**: Accepts the report number, page, and page size to customize the URL.
- **Return Value**: Constructs and returns a fully qualified URL string for accessing report data.

### `get_total_pages(url)`
Determines the total number of pages for a report by making an initial request to the report's URL and parsing the pagination details.

- **Asynchronous Operation**: Uses `httpx` to asynchronously fetch the initial page and extract the total number of pages from the pagination information.

### `generate_all_urls_async()`
Asynchronously prepares all URLs needed for downloading the reports, ensuring efficient handling of reports with multiple pages.

- **Concurrent URL Generation**: Utilizes `asyncio` tasks to simultaneously generate URLs for all pages of each report, significantly speeding up the preparation phase.

### `fetch_with_retry(url, url_index, total_urls, report_name)`
Attempts to download data from a given URL with retries on failure, reducing the impact of network issues or server errors.

- **Retry Logic**: Implements exponential backoff retry logic to handle temporary connectivity issues or server-side rate limiting.
- **Progress Logging**: Provides detailed logging for each attempt, including success notifications and warnings on retry.

### `fetch_and_merge_data()`
Coordinates the asynchronous fetching of data for all prepared URLs and merges the results into coherent datasets.

- **Asynchronous Fetching and Merging**: Leverages concurrency to download data from multiple URLs simultaneously, followed by merging the data from different pages into a single dataset per report.
- **Immediate CSV Saving**: Saves merged data to CSV files in the `Output_Data` directory right after processing each report, ensuring data persistence and easy access.

### `combine_data(pages_data)`
Combines data from multiple pages of a report into a single dataset.

- **Data Aggregation**: Aggregates items from the JSON responses of each page into a unified list, preparing it for conversion into a DataFrame.

### `save_data_to_csv(df, report_name)`
Saves the merged data for a report to a CSV file, organizing the output in a structured manner.

- **Output Directory Management**: Checks for the existence of the `Output_Data` directory and creates it if necessary.
- **CSV File Creation**: Writes the DataFrame to a CSV file named after the report, ensuring data from different reports are easily distinguishable and accessible.


## Dependencies

- Python 3
- pandas
- httpx

Ensure you have the latest versions of these dependencies installed to avoid any compatibility issues.

```python
pip install pandas
pip install httpx
```

## List of reports currently in `report_list.csv`:

| report_id | name                                                   |
|-----------|--------------------------------------------------------|
| BM-010    | Daily_Load_Forecast_Summary                            |
| BM-013    | Four_Day_Aggregated_Wind_Forecast                      |
| BM-014    | Forecast_Imbalance                                     |
| BM-016    | Aggregated_Wind_Forecast                               |
| BM-021    | Anonymised_IncDec_Curve                                |
| BM-023    | Final_Physical_Notificaiton                            |
| BM-025    | Imbalance_Price_Report(Imbalance_Pricing_Period)       |
| BM-026    | Imbalance_Price_Report(Imbalance_Settlement_Period)    |
| BM-033    | Forecast_Availability                                  |
| BM-036    | Demand_Control                                         |
| BM-037    | Daily_Dispatch_Instructions_D+1                        |
| BM-038    | Daily_Dispatch_Instructions_D+4                        |
| BM-084    | Trading_Day_Ex_Rate                                    |
| BM-086    | Daily_Meter_Data                                       |
| BM-087    | Interconnector_Flows_&_Residual_Capacity               |
| BM-089    | Average_System_Frequency                               |
| BM-095    | Balance_&_Imbalance_Market_Cost                        |
| BM-096    | Dispatch_Quantity                                      |
| BM-098    | Aggregated_Contracted_Generation_Quantities            |
| BM-099    | Aggregated_Contracted_Demand_Quantities                |
| BM-100    | Aggregated_Contracted_Wind_Quantities                  |
| BM-101    | Average_Outturn_Availability                           |
| BM-102    | Unit_Under_Test                                        |
| BM-107    | Generator_Unit_Technical_Characteristics_Transactions  |
---
