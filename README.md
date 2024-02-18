# SEMO Report Downloader and Historical Merger

This Python script automates the process of downloading SEMO reports and merging them with historical datasets available. This script will download all reports as specified in the `report_list.csv` file, and merges them with all downloaded and existing files within the `Downloads` & `Output_Data` folder.

It currently operates by reading the list of reports to be downloaded from the `report_list.csv`, and then utilises Selenium to navigate to the appropriate webpage using google chrome to download this.

# **How to run:**
- Ensure `report_list.csv` is located in same folder as the script being run.
- Remove or add rows to the `report_list.csv` if you need to change the report data being downloaded.
- Either run the .py script on the terminal, or run the first cell located in the .ipynb notebook to run the program.
- Wait approximately 30-60 seconds and then enjoy your new collection of merged data.
<br>

## Script Operation Description:

To run the script successfully you must have the `report_list.csv` file stored in the same location as the script being run, whether that is the .py or .ipynb file. 

Once run, the script will create two folders in the same location called `Downloads` & `Output_Data`. `Downloads` will contain all the raw data downloaded, and will create a new folder and download new files every time the script is run. This is because the SEMO webpage where the reports are downloaded from only go back for the last year. 

The merge data function will then scan every folder within `Downloads` and will merge files with the same name, removing duplicates and sorting the dataset from oldest to newest. These combined files are then saved in the folder `Output_Data` with the same file name as the ones they orginated from. It is done this way so that you can just arbitrarily run the script at infrequent time periods, and the program will sort out merging the new data with what already exists. The program will also consider data that already exists within the `Output_Data` folder, so you can delete the `Downloads` folder to save disk space at any time if you already have some instance of merged `Output_Data`.
<br>

## Features

- **Automated Web Scraping**: Downloads reports based on a predefined list in a CSV file using Selenium WebDriver.
- **Dynamic Directory Management**: Creates versioned and date-stamped directories for organizing downloaded reports.
- **Data Merging**: Merges CSV files from different download sessions into a single file per report type, removing duplicates and sorting data as required.
- **Output Organization**: Stores merged data in a designated output directory for easy access and further use.

## Functions Overview

### `main()`
The entry point of the script. Orchestrates the workflow by setting up directories, initiating the download process, and merging the downloaded data.

### `setup_and_download_reports(current_directory)`
Prepares the environment for downloading reports:
- Creates a main download directory within the current script's directory.
- Generates a versioned subdirectory for the current session's downloads.
- Downloads reports based on identifiers listed in a CSV file.

### `merge_data(current_directory)`
Merges CSV files from the download directories into consolidated files:
- Identifies and processes CSV files across all download sessions and an output directory.
- Removes duplicate entries based on specific criteria.
- Sorts data in each file based on predefined columns.

### `create_main_download_directory(current_directory)`
Creates a main directory named "Downloads" in the script's current directory, if it doesn't already exist.

### `create_versioned_download_directory(downloads_main_dir)`
Generates a uniquely named subdirectory within "Downloads" for the current session's files, incorporating the current date and a session number to avoid conflicts.

### `download_reports(download_dir, csv_file)`
Uses Selenium WebDriver to navigate to specified URLs and download reports:
- Reads a list of report identifiers and additional metadata from a CSV file.
- Visits each report's URL and downloads the report, handling dynamic web elements as necessary.

### `wait_and_click(driver, by_method, selector)`
A utility function to wait for a web element to become clickable and then click it, encapsulating common Selenium WebDriver interactions.

## Usage

1. **Prepare the CSV File**: Ensure `report_list.csv` is in the same directory as the script, with columns for `report_id`, `name`, and `chart?` indicating whether a chart download is required.
2. **Run the Script**: Execute the script with Python 3. Make sure all dependencies are installed, including Selenium and the necessary WebDriver.
3. **Check Outputs**: Access downloaded reports in the dynamically created directories within "Downloads". Merged and processed files will be available in the "Output_Data" directory.

## Dependencies

- Python 3
- Selenium
- pandas
- WebDriver Manager for Python

Ensure you have the latest versions of these dependencies installed to avoid any compatibility issues.

```python
pip install pandas
pip install selenium
pip install webdriver_manager
```

## List of reports currently in `report_list.csv`:

|-----------|--------------------------------------------------------|
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
|-----------|--------------------------------------------------------|
---
