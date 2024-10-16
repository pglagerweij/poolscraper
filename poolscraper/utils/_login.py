import requests

import re
import urllib.parse

def get_xsrf_token(input):
    pattern = r"crf%3d([^%]+)%3d"

    # Find the match
    match = re.search(pattern, input)
    
    if match:
        # Decode the URL-encoded part
        crf_value_encoded = match.group(1)
        crf_value_decoded = urllib.parse.unquote(crf_value_encoded)
        return crf_value_decoded + "="
    else:
        return None

def get_session_and_login(username:str, password:str):
    session = requests.Session()

    # Initial GET request to fetch any required cookies or tokens
    initial_url = "https://portal.koopman.nl/PoolSite/Login"
    session.get(initial_url)

    # URL of the login endpoint
    login_url = "https://portal.koopman.nl/PoolSite/screenservices/PoolSite/MainFlow/Login/ActionLoginUser"

    # Headers for the request
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://portal.koopman.nl",
        "OutSystems-locale": "en-US",
        "Referer": "https://portal.koopman.nl/PoolSite/Login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-CSRFToken": "T6C+9iB49TLra4jEsMeSckDMNhQ=",  # Update dynamically if needed
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    # JSON payload for the request
    payload = {
        "versionInfo": {
            "moduleVersion": "M_73esPE0CHnj+kiloLdZw",
            "apiVersion": "e7gXxY0H_aVHyZsIqLRNqg"
        },
        "viewName": "MainFlow.Login",
        "inputParameters": {
            "Email": username,
            "Password": password
        }
    }

    # Send the POST request
    response = session.post(login_url, headers=headers, json=payload)

    

    return session, response


