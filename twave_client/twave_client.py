"""TWave API Client"""

import time
from dateutil.parser import parse
import requests
import numpy as np
from .models import Asset, Metric, Trend, TrendData, PipeMeta
from .models import Wave, WaveMeta
from .models import Spectrum, SpectrumMeta


class TWaveClient:
    """TWave API Client"""

    def __init__(self, host='localhost:8080', token=''):
        self.host = host
        self.__token = token
        self.__base_url = f'http://{self.host}/api/v1/'

    def __request(self, url, params={}):
        params['links'] = False
        ret = requests.get(url, headers={'Authorization': 'Bearer ' + self.__token}, params=params)
        ret.raise_for_status()
        data = ret.json()

        # remove _links
        if isinstance(data, dict):
            data.pop('_links', None)
        elif isinstance(data, list):
            for item in data:
                item.pop('_links', None)
        return data

    def get_assets(self):
        """Get all assets"""
        url = f'{self.__base_url}/assets'

        ret = self.__request(url)
        return [Asset(**asset) for asset in ret]

    def get_asset(self, asset_id):
        """Get an asset given its ID"""
        url = f'{self.__base_url}/assets/{asset_id}'

        ret = self.__request(url)
        return Asset(**ret)

    def get_metrics(self, asset_id=None):
        """List asset metrics"""
        url = f'{self.__base_url}/metrics'

        params = {}
        if asset_id:
            params['asset'] = asset_id

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

    def list_pipes(self, asset_id=None):
        """List asset pipelines"""
        url = f'{self.__base_url}/pipes'
        params = {}
        if asset_id:
            params['asset'] = asset_id

        objects = self.__request(url, params)
        if objects is None:
            raise ValueError('No pipes found')

        return [PipeMeta(**pipe) for pipe in objects]

    def get_pipe_meta(self, _id):
        """Get pipeline metadata"""
        url = f'{self.__base_url}/pipes/{_id}'

        ret = self.__request(url)
        return PipeMeta(**ret)

    def list_pipe_data(self, _id, start=0, stop=time.time()):
        """List all stored pipeline data as a list of timestamps"""
        url = f'{self.__base_url}/pipes/{_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }

        ret = self.__request(url, params)
        return np.array(ret['time'])

    def list_waves(self, asset_id=None):
        """List all waveform types"""
        url = f'{self.__base_url}/waves'

        params = {}
        if asset_id is not None:
            params['asset'] = asset_id

        objects = self.__request(url, params)
        if objects is None:
            raise ValueError('No waves found')

        return [WaveMeta(**wave) for wave in objects]

    def get_wave_meta(self, _id):
        """Get waveform metadata"""
        url = f'{self.__base_url}/waves/{_id}'

        ret = self.__request(url)
        return WaveMeta(**ret)

    def list_wave_data(self, _id, start=0, stop=time.time()):
        """List all stored waveforms as a list of timestamps"""
        url = f'{self.__base_url}/waves/{_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }

        ret = self.__request(url, params)
        return np.array(ret['time'])

    def __get_wave_data(self, _id, timestamp='last'):
        if isinstance(timestamp, str) and timestamp != 'last':
            timestamp = parse(timestamp).timestamp()
        elif isinstance(timestamp, float):
            timestamp = int(timestamp)

        url = f'{self.__base_url}/waves/{_id}/data/{timestamp}'
        return self.__request(url)

    def get_wave(self, _id, timestamp='last'):
        """Get a waveform"""
        meta = self.get_wave_meta(_id)
        data = self.__get_wave_data(_id, timestamp)
        return Wave(meta, data)

    def list_spectra(self, asset_id=None):
        """List all spectrum types"""
        url = f'{self.__base_url}/spectra'

        param = {}
        if asset_id is not None:
            param['asset'] = asset_id

        objects = self.__request(url, param)
        if objects is None:
            raise Exception('No spectra found')

        return [SpectrumMeta(**spec) for spec in objects]

    def get_spec_meta(self, _id):
        """Get spectrum metadata"""
        url = f'{self.__base_url}/spectra/{_id}'

        ret = self.__request(url)
        return SpectrumMeta(**ret)

    def list_spec_data(self, id, start=0, stop=time.time()):
        """List all stored spectra as a list of timestamps"""
        url = f'{self.__base_url}/spectra/{id}/data'

        params = {
            "start": int(start),
            "stop": int(stop),
        }
        ret = self.__request(url, params)
        return np.array(ret['time'])

    def __get_spec_data(self, id, timestamp='last'):
        if isinstance(timestamp, str) and timestamp != 'last':
            timestamp = parse(timestamp).timestamp()
        elif isinstance(timestamp, float):
            timestamp = int(timestamp)

        url = f'{self.__base_url}/spectra/{id}/data/{timestamp}'
        req = self.__request(url)
        return req.json()

    def get_spectrum(self, spec_id, t='last'):
        """Get a spectrum"""
        meta = self.get_spec_meta(spec_id)
        data = self.__get_spec_data(spec_id, t)
        return Spectrum(meta, data)
