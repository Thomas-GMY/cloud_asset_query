# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
from sqlalchemy import Integer, String, JSON, Date, Text, DateTime, NUMERIC, DECIMAL, FLOAT

PLATFORMS = ('tencent', 'aliyun')

CLOUD_ASSERT_DB = {
    'host': os.getenv('CLOUD_ASSERT_HOST', ''),
    'port': os.getenv('CLOUD_ASSERT_PORT', ''),
    'password': os.getenv('CLOUD_ASSERT_PASSWORD', ''),
    'user': os.getenv('CLOUD_ASSERT_USER', ''),
    'database': os.getenv('CLOUD_ASSERT_DATABASE', ''),
}

COLUMNS_MAP = {
    'str': String,
    'int': Integer,
    'dict': JSON,
    'list': JSON,
    'date': Date,
    'datetime': DateTime,
    'text': Text,
    'bool': String,
    'numeric': NUMERIC,
    'decimal': DECIMAL,
    'float': FLOAT
}

TENCENT_REGIONS = [
    {
        "Region": "ap-beijing",
        "RegionName": "华北地区(北京)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-guangzhou",
        "RegionName": "华南地区(广州)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-hongkong",
        "RegionName": "港澳台地区(中国香港)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-shanghai",
        "RegionName": "华东地区(上海)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-shanghai-fsi",
        "RegionName": "华东地区(上海金融)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-shenzhen-fsi",
        "RegionName": "华南地区(深圳金融)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "ap-singapore",
        "RegionName": "亚太东南(新加坡)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "na-siliconvalley",
        "RegionName": "美国西部(硅谷)",
        "RegionState": "AVAILABLE"
    },
    {
        "Region": "na-toronto",
        "RegionName": "北美地区(多伦多)",
        "RegionState": "AVAILABLE"
    }
]

# todo: 补充阿里云的region
ALIYUN_REGIONS = [
    {
        'Region': 'cn-qingdao',
        'RegionName': '华北1（青岛）'
    },
    {
        'Region': 'cn-beijing',
        'RegionName': '华北2（北京）'
    }
]
