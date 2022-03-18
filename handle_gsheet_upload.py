from NSE_option_chain import handle_NSE_data_gather
import pygsheets
from pygsheets.exceptions import WorksheetNotFound
import pandas as pd
import os

def get_worksheet(gsheet, sheet_name):
    try:
        worksheet = gsheet.worksheet_by_title(sheet_name)
        gsheet.del_worksheet(worksheet)
        worksheet = gsheet.add_worksheet(sheet_name)
    except WorksheetNotFound:
        worksheet = gsheet.add_worksheet(sheet_name)
    return worksheet

def add_chart_to_worksheet(worksheet, df, strike_price_column, chng_in_OI_columns, anchor_cell):
    no_of_rows = df.shape[0]
    worksheet.add_chart((f'{strike_price_column}1', f'{strike_price_column}{no_of_rows}'), #X-Axis
                        [(f'{chng_in_OI_columns[0]}1', f'{chng_in_OI_columns[0]}{no_of_rows}'), (f'{chng_in_OI_columns[1]}1', f'{chng_in_OI_columns[1]}{no_of_rows}')], #Y-Axis
                        'Change in OI', #Title
                        anchor_cell = anchor_cell)


def upload_to_google_sheet(gsheet, tickers, data_dict):
    for ticker in tickers:
        df = data_dict[ticker]['df']
        meta_data = {'value': [data_dict[ticker]['value']],
                     'time': data_dict[ticker]['time']}
        meta_df = pd.DataFrame(meta_data)

        print(f"\n---Uploading {ticker} data---")
        worksheet = get_worksheet(gsheet, ticker)

        # worksheet.clear('A1', 'F70')  # Clear data from previous upload
        # worksheet.clear()
        worksheet.set_dataframe(meta_df, 'G1')  # Set value and timestamp data
        worksheet.set_dataframe(df, 'A1')  # Set Option Chain Data
        add_chart_to_worksheet(worksheet, df, 'C', ('B', 'D'), 'G4')
        

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
