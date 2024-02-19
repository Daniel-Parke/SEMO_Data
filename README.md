# SEMO Report Downloader and Historical Merger

This Python script automates the process of downloading SEMO reports and merging them with historical datasets available. This script will download all reports as specified in the `report_list.csv` file, merges where applicable, and then saves the downloaded files to the `Output_Data` folder.

# **How to run:**
- Ensure `report_list.csv` is located in same folder as the script being run.
- Run the .py script on the terminal, or run the first cell located in the .ipynb notebook to run the program.
- Wait approximately 30-60 seconds and then enjoy your new collection of merged data.

- (OPTIONAL) Remove or add rows to the `report_list.csv` if you need to change the report data being downloaded, otherwise just run the script and you should be good to go!
<br>

## Script Operation Description:

To run the script successfully you must have the `report_list.csv` file stored in the same location as the script being run, whether that is the .py or .ipynb file. 

Once run, the script will create two folders in the same location called `Downloads` & `Output_Data`. `Downloads` will contain all the raw data downloaded, and will create a new folder and download new files every time the script is run. This is because the SEMO webpage where the reports are downloaded from only go back for the last year. 

The merge data function will then scan every folder within `Downloads` and will merge files with the same name, removing duplicates and sorting the dataset from oldest to newest. These combined files are then saved in the folder `Output_Data` with the same file name as the ones they orginated from. 

It is done this way so that you can just arbitrarily run the script at infrequent time periods, and the program will sort out merging the new data with what already exists. The program will also consider data that already exists within the `Output_Data` folder, so you can delete the `Downloads` folder to save disk space at any time if you already have some instance of merged `Output_Data`.
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

## Usage

1. **Prepare the CSV File**: Ensure `report_list.csv` is in the same directory as the script, with columns for `report_id`, `name`, and `chart?` indicating whether a chart download is required.
2. **Run the Script**: Execute the script with Python 3. Make sure all dependencies are installed, including Selenium and the necessary WebDriver.
3. **Check Outputs**: Access downloaded reports in the dynamically created directories within "Downloads". Merged and processed files will be available in the "Output_Data" directory.

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
