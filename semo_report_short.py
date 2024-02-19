from SEMO_Downloader.semo_report_download import ReportURLs

async def main():
    report_urls = ReportURLs(report_list_path='SEMO_Downloader/report_list_short.csv')
    await report_urls.async_init()
    print("***********************************************************************")
    print("Reports successfully downloaded!!!")
    print("************************************************************************")
    return 

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())