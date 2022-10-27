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
        r = requests.get(url, headers={'Authorization': 'Bearer ' + self.__token}, params=params)
        r.raise_for_status()
        return r

    def list_assets(self):
        """List asset IDs"""
        url = f'{self.__base_url}/assets'
        r = self.__request(url)
        doc = r.json()
        return doc['assets']

    def get_asset(self, asset_id):
        """Get an asset given its ID"""
        url = f'{self.__base_url}/assets/{asset_id}'
        r = self.__request(url)
        return Asset(**r.json())

    def get_metrics(self, asset_id):
        """List asset metrics"""
        url = f'{self.__base_url}/assets/{asset_id}/metrics'
        r = self.__request(url)
        return r.json()

    def get_metric(self, asset_id, metric_id):
        """Get a metric"""
        url = f'{self.__base_url}/assets/{asset_id}/metrics/{metric_id}'
        r = self.__request(url)
        return Metric(**r.json())

    def __get_trend_data(self, asset_id, metric_id, start=0, stop=time.time(),
        window='1h', method='max'):

        url = f'{self.__base_url}/assets/{asset_id}/metrics/{metric_id}/trend'
        params = {
            "start": int(start),
            "stop": int(stop),
            "window": window,
            "method": method,
        }
        r = self.__request(url, params)
        return TrendData(**r.json())

    def get_trend(self, asset_id, metric_id, **args):
        """Get a metric's trend"""
        meta = self.get_metric(asset_id, metric_id)
        data = self.__get_trend_data(asset_id, metric_id, **args)
        return Trend(meta, data)

    def list_pipes(self, asset_id):
        """List asset pipelines"""
        url = f'{self.__base_url}/assets/{asset_id}/pipes'
        r = self.__request(url)
        r.raise_for_status()
        objects = r.json()
        if objects is None:
            raise Exception('No pipes found')

        return [o['id'] for o in objects]

    def get_pipe_meta(self, asset_id, pipe_id):
        """Get pipeline metadata"""
        url = f'{self.__base_url}/assets/{asset_id}/pipes/{pipe_id}'
        r = self.__request(url)
        meta = PipeMeta(**r.json())
        return meta

    def list_pipe_data(self, asset_id, pipe_id, start=0, stop=time.time()):
        """List all stored pipeline data as a list of timestamps"""
        url = f'{self.__base_url}/assets/{asset_id}/pipes/{pipe_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }
        r = self.__request(url, params)

        ret = r.json()
        return ret['time']

    def list_waves(self, asset_id):
        """List all waveform types"""
        url = f'{self.__base_url}/assets/{asset_id}/waves'
        r = self.__request(url)
        r.raise_for_status()
        objects = r.json()
        if objects is None:
            raise Exception('No waves found')

        return [o['id'] for o in objects]

    def get_wave_meta(self, asset_id, wave_id):
        """Get waveform metadata"""
        url = f'{self.__base_url}/assets/{asset_id}/waves/{wave_id}'
        r = self.__request(url)
        return WaveMeta(**r.json())

    def list_wave_data(self, asset_id, wave_id, start=0, stop=time.time()):
        """List all stored waveforms as a list of timestamps"""
        url = f'{self.__base_url}/assets/{asset_id}/waves/{wave_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }
        r = self.__request(url, params)
        r.raise_for_status()
        ret = r.json()
        return np.array(ret['time'])

    def __get_wave_data(self, asset_id, wave_id, timestamp='last'):
        if isinstance(timestamp, str) and timestamp != 'last':
            timestamp = parse(timestamp).timestamp()
        elif isinstance(timestamp, float):
            timestamp = int(timestamp)

        url = f'{self.__base_url}/assets/{asset_id}/waves/{wave_id}/data/{timestamp}'
        r = self.__request(url)
        r.raise_for_status()
        return r.json()

    def get_wave(self, asset_id, wave_id, timestamp='last'):
        """Get a waveform"""
        meta = self.get_wave_meta(asset_id, wave_id)
        data = self.__get_wave_data(asset_id, wave_id, timestamp)
        return Wave(meta, data)

    def list_spectra(self, asset_id):
        """List all spectrum types"""
        url = f'{self.__base_url}/assets/{asset_id}/spectra'
        objects = self.__request(url).json()
        if objects is None:
            raise Exception('No spectra found')

        return [o['id'] for o in objects]

    def get_spec_meta(self, asset_id, spec_id):
        """Get spectrum metadata"""
        url = f'{self.__base_url}/assets/{asset_id}/spectra/{spec_id}'
        r = self.__request(url)
        return SpectrumMeta(**r.json())

    def list_spec_data(self, asset_id, spec_id, start=0, stop=time.time()):
        """List all stored spectra as a list of timestamps"""
        url = f'{self.__base_url}/assets/{asset_id}/spectra/{spec_id}/data'
        params = {
            "start": int(start),
            "stop": int(stop),
        }
        r = self.__request(url, params)
        r.raise_for_status()

        ret = r.json()
        return np.array(ret['time'])

    def __get_spec_data(self, asset_id, spec_id, timestamp='last'):
        if isinstance(timestamp, str) and timestamp != 'last':
            timestamp = parse(timestamp).timestamp()
        elif isinstance(timestamp, float):
            timestamp = int(timestamp)

        url = f'{self.__base_url}/assets/{asset_id}/spectra/{spec_id}/data/{timestamp}'
        r = self.__request(url)
        return r.json()

    def get_spectrum(self, asset_id, spec_id, t='last'):
        """Get a spectrum"""
        meta = self.get_spec_meta(asset_id, spec_id)
        data = self.__get_spec_data(asset_id, spec_id, t)
        return Spectrum(meta, data)
