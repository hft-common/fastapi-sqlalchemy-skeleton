import datetime
import os
import zipfile

import pandas as pd
import pandas_ta as ta
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from fastapi.params import File
from decorators.handle_generic_exception import frontend_api_generic_exception
import tempfile

from external_services.lime_apis.lime_apis import lime_create_new_token, get_open_value_according_to_datetime

excel_router = APIRouter(prefix='/excel-data', tags=['auth'])

headers = {
    "Content-Disposition": "attachment",
    "Content-Type": "text/csv",
}


@excel_router.post('/update')
@frontend_api_generic_exception
def edit_excel_data(file: UploadFile = File(None)):
    df = pd.DataFrame()  # Empty DataFrame

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    # Load data
    df = pd.read_csv(temp_file_path, sep=",")

    token = lime_create_new_token()
    if token['status_code'] == 200:
        bearer_token = token['access_token']
    else:
        return {"error": True, "error_message": "Authorisation Error"}

    for index, row in df.iterrows():
        date_string = row['Date']
        date_format = "%d-%m-%Y"
        date_obj = datetime.datetime.strptime(str(date_string), date_format)

        # Convert date object to timestamp
        from_timestamp = int(date_obj.timestamp())

        # Get current date and time
        current_datetime = datetime.datetime.now()
        # Convert current datetime to timestamp
        converted_timestamp = int(current_datetime.timestamp())
        period = 'minute_'+str(int(row['Time Frame']))
        get_date_wise_data = get_open_value_according_to_datetime(bearer_token=bearer_token, symbol=row['Stock'],
                                                                  period=period,
                                                                  from_date=from_timestamp,
                                                                  to_date=converted_timestamp)

        if get_date_wise_data['status_code'] == 200:
            get_date_wise_data = get_date_wise_data['values']
        else:
            return {"error": True, "error_message": get_date_wise_data['status_code']}

        get_date_wise_data_df = pd.DataFrame(get_date_wise_data)

        get_date_wise_data_df['timestamp'] = pd.to_datetime(get_date_wise_data_df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        get_date_wise_data_df.set_index('timestamp', inplace=True)

        # Calculate VWAP using pandas_ta
        vwap = ta.vwap(get_date_wise_data_df['high'], get_date_wise_data_df['low'], get_date_wise_data_df['close'],
                              get_date_wise_data_df['volume'])

        # Add VWAP to the DataFrame
        get_date_wise_data_df['vwap'] = vwap
        vwap_std = vwap.rolling(window=20).std()  # Replace 'n' with the desired window size for standard deviation

        # Define a multiplier for the standard deviation
        std_multiplier = 3
        multiplier = 3

        # Calculate VWAP Upper and Lower
        vwap_upper = vwap + (std_multiplier * vwap_std)
        vwap_lower = vwap - (multiplier * vwap_std)

        # Calculate and add ATR
        get_date_wise_data_df['ATR'] = ta.atr(get_date_wise_data_df['high'], get_date_wise_data_df['low'],
                                              get_date_wise_data_df['close'],
                                              length=14)

        # Add VWAP Upper and Lower to the DataFrame
        get_date_wise_data_df['vwap_upper'] = vwap_upper
        get_date_wise_data_df['vwap_lower'] = vwap_lower
        get_date_wise_data_df.reset_index(inplace=True)

        # Generate csv file name
        csv_file_name = row['Stock'] + '_' + str(date_string) + '_to_' + str(current_datetime.date()) +'.csv'

        counter = 1
        while os.path.exists(csv_file_name):
            base_name, extension = os.path.splitext(csv_file_name)
            csv_file_name = f"{base_name}_{counter}{extension}"
            counter += 1

        get_date_wise_data_df.to_csv(csv_file_name, index=False)
    return {"error": False, "message": "Successfully get data in csv"}
