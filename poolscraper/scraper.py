from .utils._login import get_session_and_login, get_xsrf_token
from .utils._retrieve_cars import retrieve_cars

def get_cars(username, password):
    xsrf_token = None
    while xsrf_token is None: 
        session, login_response = get_session_and_login(username=username, password=password)
        xsrf_token = get_xsrf_token(session.cookies.get('nr2Users'))
    # print(login_response.text)
    output = retrieve_cars(session=session, login_response=login_response)

    json_output = output.json()

    cars_list_json = json_output.get('data').get('List').get('List')

    cars_list = []

    for car in cars_list_json:
        unique_atl_car_id = car.get('VoertuigATLInfo').get('Id')
        output_info = {
            "id": unique_atl_car_id,
            "merk": car.get('VoertuigATLInfo').get('merk'),
            "model": car.get('VoertuigATLInfo').get('model'),
            "kenteken": car.get('VoertuigRDWInfo').get('Kenteken'),
            "eerste_toelating": car.get('VoertuigRDWInfo').get('datumEersteToelatingNat'),
            "car_category": car.get('FleetOwnerCategorie').get('Naam'),
            "catalogusPrijs": car.get('VoertuigRDWInfo').get('catalogusPrijs'),
        }
        cars_list.append(output_info)

    return cars_list

