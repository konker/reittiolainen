#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# reittiolainen
# 
# A command line interface to reittiopas.com
#
# Authors: Konrad Markus <konker@gmail.com>
#

import json

ENDPOINT = 'http://api.reittiopas.fi/hsl/prod/'

ROUTE_FORMATS = ['json', 'xml', 'txt']
ROUTE_FORMATS_DEFAULT = 'json'

ROUTE_LANGUAGES = ['fi', 'sv', 'en', 'slangi']
ROUTE_LANGUAGES_DEFAULT = 'fi'

ROUTE_TIMETYPES = ['departure', 'arrival']
ROUTE_TIMETYPES_DEFAULT = 'departure'

ROUTE_ZONES = ['helsinki', 'espoo', 'vantaa', 'region', 'whole']
ROUTE_ZONES_DEFAULT = ''

ROUTE_TRANSPORT_TYPES = ['all', 'bus', 'train', 'metro', 'tram', 'service', 'uline', 'ferry', 'walk']
ROUTE_TRANSPORT_TYPES_DEFAULT = 'all'

ROUTE_DETAIL_LEVELS = ['limited', 'normal', 'full']
ROUTE_DETAIL_LEVELS_DEFAULT = 'normal'

GEOCODE_CITIES = ['espoo', 'helsinki']
GEOCODE_CITIES_DEFAULT = ''

GEOCODE_LOCATION_TYPES = ['stop', 'address']
GEOCODE_LOCATION_TYPES_DEFAULT = ''


class Reittiopas(object):
    def __init__(self, endpoint, username, password,
                 format=ROUTE_FORMATS_DEFAULT, language=ROUTE_LANGUAGES_DEFAULT):
        self.endpoint = endpoint
        self.username = username
        self.password = password

        self.format = format
        self.language = language

    def route(self, from_coord, to_coord,
              via_coord=None, date=None, time=None,
              timetype=ROUTE_TIMETYPES_DEFAULT,
              transport_types=ROUTE_TRANSPORT_TYPES_DEFAULT,
              detail_level=ROUTE_DETAIL_LEVELS_DEFAULT):

        params = {}
        params['request'] = 'route'
        params['from'] = "%s,%s" % from_coord
        params['to'] = "%s,%s" % to_coord
        if via_coord:
            params['via'] = "%s,%s" % via_coord

        if date:
            params['date'] = date

        if time:
            params['time'] = time

        params['timetype'] = timetype
        params['detail'] = detail_level

        if type(transport_types) == type({}):
            params['transport_types'] = "|".join(transport_types)
        else:
            params['transport_types'] = transport_types

        return self._request_url(params)


    def geocode(self, search_term, cities=GEOCODE_CITIES_DEFAULT, location_types=GEOCODE_LOCATION_TYPES_DEFAULT):
        params = {}
        params['request'] = 'geocode'
        params['key'] = search_term
        if type(cities) == type({}):
            params['cities'] = "|".join(cities)
        elif not cities == '':
            params['cities'] = cities

        if type(location_types) == type({}):
            params['location_types'] = "|".join(location_types)
        elif not location_types == '':
            params['location_types'] = location_types

        return self._request_url(params)


    def _request_url(self, params):
        url = "%s?user=%s&pass=%s&request=%s&format=%s&lang=%s" % (self.endpoint, self.username, self.password, params['request'], self.format, self.language)
        for (key,value) in params.items():
            # TODO: urlencode values
            url += "&%s=%s" % (key, value)
            
        return url

def main():
    reittiopass = Reittiopas(ENDPOINT, 'konker', '----')
    reittiopass.format = 'txt'
    reittiopass.language = 'en'
    print(reittiopass.geocode("Tekniikatie 14, Espoo"))
    print(reittiopass.geocode("Fredrikinktu 63, Helsinki"))
    print(reittiopass.route((2545972,6674578), (2551796,6673513)))


if __name__ == '__main__':
    try:
	    main()
    except KeyboardInterrupt:
        logging.info('Interrupted, exiting')
        exit(1)


