from NSE_option_chain import handle_NSE_data_gather
import pygsheets
from pygsheets.exceptions import WorksheetNotFound
import pandas as pd
import os


def upload_to_google_sheet(gsheet, tickers, data_dict):
    for ticker in tickers:
        df = data_dict[ticker]['df']
        meta_data = {'value': [data_dict[ticker]['value']],
                     'time': data_dict[ticker]['time']}
        meta_df = pd.DataFrame(meta_data)

        print(f"\n---Uploading {ticker} data---")
        try:
            worksheet = gsheet.worksheet_by_title(ticker)
        except WorksheetNotFound:
            worksheet = gsheet.add_worksheet(ticker)

        worksheet.clear('A1', 'F70')  # Clear data from previous upload
        worksheet.set_dataframe(meta_df, 'A1')  # Set value and timestamp data
        worksheet.set_dataframe(df, 'A4')  # Set Option Chain Data


def get_NSE_data_and_upload(indexes, equities):
    equities_dict = {}
    indexes_dict = {}

    for equity in equities:
        placeholder = dict()
        print(f"\n---Gathering {equity} data---")
        option_data = handle_NSE_data_gather(equity, 'equities')
        placeholder[equity] = option_data
        equities_dict.update(placeholder)

    for index in indexes:
        placeholder = dict()
        print(f"\n---Gathering {index} data---")
        option_data = handle_NSE_data_gather(index, 'indices')
        placeholder[index] = option_data
        indexes_dict.update(placeholder)

    # Stored GCP creds json filepath in .env
    GCP_CREDS = os.environ.get('GCP_CREDS')
    gc = pygsheets.authorize(service_file=GCP_CREDS)

    sh = gc.open('Stonks')  # Open the Google Sheet
    upload_to_google_sheet(sh, indexes, indexes_dict)
    upload_to_google_sheet(sh, equities, equities_dict)
