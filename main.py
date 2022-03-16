from handle_user_input import get_stocks_from_user
from dotenv import load_dotenv
from handle_gsheet_upload import get_NSE_data_and_upload


def main():
    load_dotenv()  # Load environment variables
    # CAN TAKE USER INPUT OR DEFINE HARDCODE
    indexes, equities = get_stocks_from_user()

    # indexes = ['BANKNIFTY']
    # equities = ['FEDERALBNK']

    get_NSE_data_and_upload(indexes, equities)


if __name__ == "__main__":
    main()
