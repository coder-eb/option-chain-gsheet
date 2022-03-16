import requests
import pandas as pd
from requests.exceptions import JSONDecodeError
import os


def create_dataframe_from_api_data(api_data):
    filtered_data = api_data['filtered']
    options_data = filtered_data['data']

    headers = ['CopenInterest', 'CchangeinOpenInterest',
               'strikePrice', 'PchangeinOpenInterest', 'PopenInterest']
    records = []

    for record in options_data:
        record_data = [record['CE']['openInterest'], record['CE']['changeinOpenInterest'],
                       record['strikePrice'],
                       record['PE']['changeinOpenInterest'], record['PE']['openInterest']]

        records.append(record_data)

    tot_data = [filtered_data['CE']['totOI'],
                0, 0, 0,
                filtered_data['PE']['totOI']]
    records.append(tot_data)

    df = pd.DataFrame(columns=headers, data=records)
    return df


def req_NSE_data(url):
    headers = {
        'User-Agent': 'Chrome/99.0.4844.51'
    }

    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except JSONDecodeError:
        print(f"\n\n---UNABLE TO ACCESS RESOURCE---")
        print(f"\nTry opening the below link in browser and run code again")
        print(f"\n\n{url}")
        quit()


def get_NSE_data(ticker, url_option):
    BASE_URL = os.environ('BASE_URL')
    url = f"{BASE_URL}/api/option-chain-{url_option}?symbol={ticker}"
    print(f"------MAKING REQUEST TO-----\n{url}")
    return req_NSE_data(url)


def handle_NSE_data_gather(ticker, url_option):
    option_chain_data = {}
    api_data = get_NSE_data(ticker, url_option)
    option_chain_data['df'] = create_dataframe_from_api_data(api_data)
    option_chain_data['time'] = api_data['records']['timestamp']
    option_chain_data['value'] = api_data['records']['underlyingValue']
    return option_chain_data
