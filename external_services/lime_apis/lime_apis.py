import requests
import config


def lime_create_new_token():
    config.default_log.debug("Inside lime_create_new_token")
    url = "https://auth.lime.co/connect/token"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'password',
        'client_id': config.lime_client_id,
        'client_secret': config.lime_client_secret,
        'username': config.lime_username,
        'password': config.lime_password
    }

    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    status_code = response.status_code
    if status_code == 200:
        config.default_log.debug("Request successful")
        json_response = response.json()
        access_token = json_response['access_token']
        config.default_log.debug("Access Token:", access_token)
        return dict(access_token=access_token, status_code=status_code)
    else:
        config.default_log.debug(f"Request failed with status code {response.status_code}")
        return dict(status_code=status_code)


def get_open_value_according_to_datetime(bearer_token, symbol, period, from_date, to_date):
    config.default_log.debug(f"Inside get_open_value_according_to_datetime")
    url = 'https://api.lime.co/marketdata/history'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+bearer_token
    }

    params = {
        'symbol': symbol,
        'period': period,
        'from': from_date,
        'to': to_date
    }

    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        config.default_log.debug("Request successful")
        response_data = response.json()

        # Extract values
        values = [entry for entry in response_data]
        return dict(values=values, status_code=response.status_code)
    else:
        config.default_log.debug(f"Request failed with status code {response.status_code}")
        return dict(status_code=response.status_code, error_message=response.json())
