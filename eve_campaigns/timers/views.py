from django.shortcuts import render

# Create your views here.

import urllib3
import json
import calendar
import time
import datetime
# define objects

http = urllib3.PoolManager()


def index(request):
    campaign_endpoint = 'https://esi.evetech.net/latest/sovereignty/campaigns/?datasource=tranquility'
    campaign_request = http.request('GET', campaign_endpoint)
    campaign_json = json.loads(campaign_request.data)
    timer_list = []
    for timer in campaign_json:
        structure_type = timer['event_type'].title().replace('_', ' ')
        const_id = timer['constellation_id']
        defender_id = timer['defender_id']
        system_id = timer['solar_system_id']

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
        start_time = timestamp_fixer(timer['start_time'])

        timer = {
            'structure_type': structure_type,
            'const_name': const_name,
            'region_name': region_name,
            'defender_name': defender_name,
            'system_name': system_name,
            'start_time': start_time,
        }
        timer_list.append(timer)

    context = {}
    context['timer_list'] = timer_list
    return render(request, 'timers/index.html', context=context)


def timestamp_fixer(timestamp):
    td = timestamp.split("T", 1)
    tdd = f"{td[0]} {td[1]}"
    tss = tdd.split("Z", 1)
    iso_stamp = tss[0]

    now = time.gmtime()
    now_secs = calendar.timegm(now)
    now_stamp = datetime.datetime.utcfromtimestamp(now_secs)
    timer_time = datetime.datetime.fromisoformat(iso_stamp)
    t_delta = timer_time - now_stamp

    ts_delta = str(t_delta)
    tss_delta = ts_delta.split(":", 2)
    delta_string = f"{tss_delta[0]}h {tss_delta[1]}m {tss_delta[2]}s"
    return delta_string

