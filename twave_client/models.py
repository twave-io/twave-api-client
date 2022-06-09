"""TWave API data models"""

from dataclasses import dataclass, field
from base64 import b64decode
from typing import List, Dict
import numpy as np


def _decode_array(data, fmt='int16_zlib'):
    bindata = b64decode(data)

    if fmt == 'float32':
        return np.frombuffer(bindata, dtype=np.float32)
    else:
        raise ValueError("Unknown data format: %s" % fmt)


@dataclass
class Asset(object):
    id: str
    version: int
    created_at: int
    updated_at: int
    name: str
    display_name: Dict[str, str]
    description: Dict[str, str]
    tags: List[str]


@dataclass
class Metric(object):
    id: str
    asset_id: str
    name: str
    data_type :str = 'float'
    enum_type: str = ''
    unit: str = ''
    limit_min: float = 0
    limit_max: float = 0
    has_alarm: bool = False
    aggregate: str = 'mean'
    format: str = ''
    suffix: str = ''
    tags: list = field(default_factory=list)


@dataclass
class TrendData(object):
    id: str
    start: str
    stop: str
    time: List[int]
    value: List[float]
    agg_window: str
    agg_method: str = 'mean'


@dataclass
class PipeMeta(object):
    id: str
    asset_id: str
    created_at: int
    name: str
    metrics: List[float]


@dataclass
class WaveMeta(object):
    id: str
    asset_id: str
    created_at: int
    name: str
    sample_rate: float
    samples: int = 0
    unit: str = ''
    synchronous: bool = False
    data_format: str = 'float32'


@dataclass
class SpectrumMeta(object):
    id: str
    asset_id: str
    created_at: int
    name: str
    bins: int
    max_freq: float
    min_freq: float = 0.0
    unit: str = ''
    suffix: str = ''
    window: str = 'hann'
    data_format: str = 'float32'
    synchronous: bool = False
    full: bool = False


class Trend(object):
    def __init__(self, meta, data):
        self.meta = meta
        self.__data = data

    def get_data(self):
        return np.array(self.__data.time), np.array(self.__data.value)


class Wave(object):
    def __init__(self, meta, data):
        self.meta = meta
        self.__data = _decode_array(data['data'], meta.data_format)

    def get_duration(self):
        return len(self.__data)/self.meta.sample_rate

    def get_data(self):
        n = len(self.__data)
        x = np.linspace(0, n/self.meta.sample_rate, n)
        return x, self.__data


class Spectrum(object):
    def __init__(self, meta, data):
        self.meta = meta
        self.__data = _decode_array(data['data'], self.meta.data_format)

    def get_data(self):
        freq = np.linspace(self.meta.min_freq, self.meta.max_freq, len(self.__data))
        return freq, self.__data
