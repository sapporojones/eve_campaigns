import urllib3
import json


# define objects

http = urllib3.PoolManager()

"""
An example object from the endpoint:

  {
    "attackers_score": 0.4,
    "campaign_id": 98927,
    "constellation_id": 20000177,
    "defender_id": 99010549,
    "defender_score": 0.6,
    "event_type": "ihub_defense",
    "solar_system_id": 30001216,
    "start_time": "2022-10-29T09:11:52Z",
    "structure_id": 1037908970273
  }
  
  required resolves: constellation_id, defender_id, solar_system_id, 
  todo: campaign_id(?), 
"""


def value_resolver(const_id, defender_id, system_id):
    const_url = f'https://esi.evetech.net/latest/universe/constellations/{const_id}/?datasource=tranquility&language=en'
    defender_url = f'https://esi.evetech.net/latest/alliances/{defender_id}/?datasource=tranquility'
    system_url = f'https://esi.evetech.net/latest/universe/systems/{system_id}/?datasource=tranquility&language=en'

    const_req = http.request('GET', const_url)
    const_json = json.loads(const_req.data)
    region_id = const_json['region_id']
    const_name = const_json['name']

    region_url = f'https://esi.evetech.net/latest/universe/regions/{region_id}/?datasource=tranquility&language=en'
    region_req = http.request('GET', region_url)
    region_json = json.loads(region_req.data)
    region_name = region_json['name']

    defender_req = http.request('GET', defender_url)
    defender_json = json.loads(defender_req.data)
    defender_name = defender_json['name']

    system_req = http.request('GET', system_url)
    system_json = json.loads(system_req.data)
    system_name = system_json['name']

    return const_name, defender_name, system_name, region_name


def main():
    campaign_endpoint = 'https://esi.evetech.net/latest/sovereignty/campaigns/?datasource=tranquility'
    campaign_request = http.request('GET', campaign_endpoint)
    campaign_json = json.loads(campaign_request.data)
    for timer in campaign_json:
        structure_type = timer['event_type'].title().replace('_', ' ')
        constellation, defender, systemid, region = value_resolver(
            timer['constellation_id'],
            timer['defender_id'],
            timer['solar_system_id'],
        )
        start_time = timer['start_time']
        print(f'{start_time} - {structure_type} - {region} - {constellation} - {systemid} - {defender}')


if __name__ == '__main__':
    main()