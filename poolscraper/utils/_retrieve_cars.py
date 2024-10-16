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

def fetch_client_variables_from_login_response(login_response):
    json_response = login_response.json()
    return {
            "RegistrantId": json_response.get("data").get("Registrant").get("Id"),
            "LegalEntityId": json_response.get("data").get("Registrant").get("LegalEntityId"),
            "Locale": json_response.get("data").get("Registrant").get("Locale"),
            "Username": json_response.get("data").get("Registrant").get("Name")
        }


def retrieve_cars(session, login_response):
    # URL of the endpoint
    url = "https://portal.koopman.nl/PoolSite/screenservices/PoolSite/MainFlow/Home/ScreenDataSetGetVehiclesForFleetOwner"
    csrf_token = get_xsrf_token(session.cookies.get('nr2Users'))

    # Headers for the request
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://portal.koopman.nl",
        "OutSystems-locale": "nl-NL",
        "Referer": "https://portal.koopman.nl/PoolSite/Home",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-CSRFToken": csrf_token,
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    # JSON payload for the request
    payload = {
        "versionInfo": {
            "moduleVersion": "M_73esPE0CHnj+kiloLdZw",
            "apiVersion": "g9UmGleppOCdSaPClw9r4w"
        },
        "viewName": "MainFlow.Home",
        "screenData": {
            "variables": {}
        },
        "inputParameters": {
            "StartIndex": 0,
            "MaxRecords": 1000
        },
        "clientVariables": fetch_client_variables_from_login_response(login_response=login_response)
    }

    # Send the POST request
    return session.post(url, headers=headers, json=payload)