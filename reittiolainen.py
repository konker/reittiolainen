#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# reittiolainen
# 
# A command line interface to reittiopas.com
#
# Authors: Konrad Markus <konker@gmail.com>
#

import re
import json
import urllib
import urllib2


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

        return self._make_request(self._request_url(params))


    def geocode_coords(self, search_term):
        return self._get_coords(self.geocode(search_term))


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
        else:
            if re.match("^\w?\d+$", params['key']):
                params['location_types'] = 'stop'
            else:
                params['location_types'] = 'address'

        return self._make_request(self._request_url(params))


    def _get_coords(self, response):
        if len(response) > 0:
            return tuple(response[0]['coords'].split(','))
        return None

    def _make_request(self, url):
        print(url)
        try:
            f = urllib2.urlopen(url)
        except urllib2.HTTPError as ex:
            print(str(ex))
            exit(-1)

        if self.format == 'txt':
            return f.read()
        elif self.format == 'json':
            return json.load(f)
        else:
            #[FIXME: xml handling]
            return None


    def _request_url(self, params):
        url = "%s?user=%s&pass=%s&request=%s&format=%s&lang=%s" % (self.endpoint, self.username, self.password, params['request'], self.format, self.language)
        for (key,value) in params.items():
            # TODO: urlencode values
            url += "&%s=%s" % (urllib.quote(key), urllib.quote(value))
            
        return url


def main():
    reittiopass = Reittiopas(ENDPOINT, 'konker', 'pppp')
    reittiopass.format = 'json'
    reittiopass.language = 'en'
    fr = reittiopass.geocode_coords("Tekniikatie 14, Espoo")
    to = reittiopass.geocode_coords("Fredrikinktu 63, Helsinki")
    route = reittiopass.route(fr, to, time='1700', detail_level='limited')
    for rr in route:
        print("====")
        for r in rr:
            print("---")
            for l in r['legs']:
                print(l['type'])


if __name__ == '__main__':
    try:
	    main()
    except KeyboardInterrupt:
        logging.info('Interrupted, exiting')
        exit(1)


