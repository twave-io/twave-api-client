"""TWave API Client"""

import time
from enum import Enum
from dateutil.parser import parse
import requests
import numpy as np
from .models import Asset, Metric, Trend, TrendData, PipeMeta
from .models import Wave, WaveMeta
from .models import Spectrum, SpectrumMeta

# create an enumeration of the object types
class ObjectType(Enum):
    PIPE = 0
    WAVE = 1
    SPEC = 2

    def __str__(self):
        return {
            ObjectType.PIPE: 'pipe',
            ObjectType.WAVE: 'wave',
            ObjectType.SPEC: 'spectrum',
        }[self]

    def uri_name(self):
        """Return the name of the object type in the URI"""
        return {
            ObjectType.PIPE: 'pipes',
            ObjectType.WAVE: 'waves',
            ObjectType.SPEC: 'spectra',
        }[self]


class TWaveClient:
    """TWave API Client"""

    def __init__(self, host='localhost:8080', token=''):
        self.host = host
        self.__token = token
        self.__base_url = f'http://{self.host}/api/v1'

    def __request(self, url, params=None, method='GET'):
        par = {'links': 'false'}
        if params:
            par.update(params)

        headers = {'Authorization': 'Bearer ' + self.__token}
        ret = requests.request(method, url, params=par, headers=headers)
        ret.raise_for_status()
        data = ret.json()

        # remove _links
        if isinstance(data, dict):
            data.pop('_links', None)
        elif isinstance(data, list):
            for item in data:
                item.pop('_links', None)
        return data

    def list_assets(self, name=None):
        """Get all assets"""
        url = f'{self.__base_url}/assets'

        params = {}
        if name:
            params['name'] = name

        ret = self.__request(url, params)
        return [Asset(**asset) for asset in ret]

    def get_asset(self, _id):
        """Get an asset given its ID"""
        url = f'{self.__base_url}/assets/{_id}'

        ret = self.__request(url)
        return Asset(**ret)

    def list_metrics(self, asset=None, name=None):
        """List asset metrics"""
        url = f'{self.__base_url}/metrics'

        params = {}
        if asset:
            params['asset'] = asset
        if name:
            params['name'] = name

        ret = self.__request(url, params)
        return [Metric(**metric) for metric in ret]

    def get_metric(self, _id):
        """Get a metric"""
        url = f'{self.__base_url}/metrics/{_id}'

        ret = self.__request(url)
        return Metric(**ret)

    def __get_trend_data(self, _id, start=0, stop=time.time(), window='1h', method='max'):
        url = f'{self.__base_url}/metrics/{_id}/trend'
        params = {
            "start": int(start),
            "stop": int(stop),
            "window": window,
            "method": method,
        }
        ret = self.__request(url, params)
        return TrendData(**ret)

    def get_trend(self, _id, **args):
        """Get a metric's trend"""
        meta = self.get_metric(_id)
        data = self.__get_trend_data(_id, **args)
        return Trend(meta, data)

    def __list_object_meta(self, _type: ObjectType, asset=None, name=None):
        """List objects of a given type"""
        url = f'{self.__base_url}/{_type.uri_name()}'
        params = {}
        if asset:
            params['asset'] = asset
        if name:
            params['name'] = name

        objects = self.__request(url, params)
        if objects is None:
            raise ValueError(f'No {_type} found')

        if _type == ObjectType.PIPE:
            return [PipeMeta(**pipe) for pipe in objects]
        elif _type == ObjectType.WAVE:
            return [WaveMeta(**wave) for wave in objects]
        elif _type == ObjectType.SPEC:
            return [SpectrumMeta(**spec) for spec in objects]
        else:
            raise ValueError(f'Unknown type {_type}')

    def __get_object_meta(self, _type: ObjectType, _id):
        """Get an object's metadata"""
        url = f'{self.__base_url}/{_type.uri_name()}/{_id}'

        ret = self.__request(url)
        if _type == ObjectType.PIPE:
            return PipeMeta(**ret)
        elif _type == ObjectType.WAVE:
            return WaveMeta(**ret)
        elif _type == ObjectType.SPEC:
            return SpectrumMeta(**ret)
        else:
            raise ValueError(f'Unknown type {_type}')

    def __list_object_data(self, _type:ObjectType, _id, start=0, stop=time.time()):
        """List objects of a given type"""
        url = f'{self.__base_url}/{_type.uri_name()}/{_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }

        ret = self.__request(url, params)
        return np.array(ret['time'])

    def __get_object_data(self, _type:ObjectType, _id, timestamp='last'):
        """Get an object's data at a given timestamp"""
        if isinstance(timestamp, str) and timestamp != 'last':
            timestamp = parse(timestamp).timestamp()
        elif isinstance(timestamp, float):
            timestamp = int(timestamp)

        url = f'{self.__base_url}/{_type.uri_name()}/{_id}/data/{timestamp}'

        #TODO: convert the data to a custom object
        return self.__request(url)

    def __delete_object_data(self, _type:ObjectType, _id, start, stop):
        """Delete an object's data in a given time range"""
        url = f'{self.__base_url}/{_type}/{_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }
        return self.__request(url, params, method='DELETE')

    # Methods for accessing pipe data

    def list_pipes(self, asset=None, name=None):
        """List pipes"""
        return self.__list_object_meta(ObjectType.PIPE, asset, name)

    def get_pipe_meta(self, _id):
        """Get a pipe's metadata"""
        return self.__get_object_meta(ObjectType.PIPE, _id)

    def list_pipe_data(self, _id, start=0, stop=time.time()):
        """List pipe data"""
        return self.__list_object_data(ObjectType.PIPE, _id, start, stop)

    def get_pipe_data(self, _id, t='last'):
        """Get pipe data at a given timestamp"""
        return self.__get_object_data(ObjectType.PIPE, _id, t)

    def delete_pipe_data(self, _id, start, stop):
        """Delete pipe data in a given time range"""
        return self.__delete_object_data(ObjectType.PIPE, _id, start, stop)

    # Methods for accessing waveform data

    def list_waves(self, asset=None, name=None):
        """List waves"""
        return self.__list_object_meta(ObjectType.WAVE, asset, name)

    def get_wave_meta(self, _id):
        """Get a wave's metadata"""
        return self.__get_object_meta(ObjectType.WAVE, _id)

    def list_wave_data(self, _id, start=0, stop=time.time()):
        """List wave data"""
        return self.__list_object_data(ObjectType.WAVE, _id, start, stop)

    def get_wave_data(self, _id, timestamp='last'):
        """Get wave data at a given timestamp"""
        return self.__get_object_data(ObjectType.WAVE, _id, timestamp)

    def get_wave(self, _id, timestamp='last'):
        """Get wave data at a given timestamp"""
        meta = self.get_wave_meta(_id)
        data = self.get_wave_data(_id, timestamp)
        return Wave(meta, data)

    def delete_wave_data(self, _id, start, stop):
        """Delete wave data in a given time range"""
        return self.__delete_object_data(ObjectType.WAVE, _id, start, stop)

    # Methods for accessing spectrum data

    def list_spectra(self, asset=None, name=None):
        """List spectra"""
        return self.__list_object_meta(ObjectType.SPEC, asset, name)

    def get_spectrum_meta(self, _id):
        """Get a spectrum's metadata"""
        return self.__get_object_meta(ObjectType.SPEC, _id)

    def list_spectrum_data(self, _id, start=0, stop=time.time()):
        """List spectrum data"""
        return self.__list_object_data(ObjectType.SPEC, _id, start, stop)

    def get_spectrum_data(self, _id, timestamp='last'):
        """Get spectrum data at a given timestamp"""
        return self.__get_object_data(ObjectType.SPEC, _id, timestamp)

    def get_spectrum(self, _id, timestamp='last'):
        """Get spectrum data at a given timestamp"""
        meta = self.get_spectrum_meta(_id)
        data = self.get_spectrum_data(_id, timestamp)
        return Spectrum(meta, data)

    def delete_spectrum_data(self, _id, start, stop):
        """Delete spectrum data in a given time range"""
        return self.__delete_object_data(ObjectType.SPEC, _id, start, stop)