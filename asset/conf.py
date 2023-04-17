# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import arrow
from sqlalchemy import Integer, String, JSON, Date, Text, DateTime, NUMERIC, DECIMAL, FLOAT
from asset.schema import TencentProfile, AliyunProfile, AwsProfile


PROVIDERS = ('tencent', 'aliyun', 'aws')
PROVIDER_PROFILES = {
    'tencent': TencentProfile,
    'aliyun': AliyunProfile,
    'aws': AwsProfile
}

today = arrow.now().datetime
yesterday = arrow.now().shift(days=-1).datetime

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

# todo: complete cloud providers`s regions
REGIONS = {
    'tencent': {
        'default_region': 'ap-shanghai',
        'regions': [
            'ap-beijing',
            'ap-guangzhou',
            'ap-hongkong',
            'ap-shanghai',
            'ap-shanghai-fsi',
            'ap-shenzhen-fsi',
            'ap-nanjing',
            'ap-chengdu',
            'ap-chongqing'
        ]
    },
    'aliyun': {
        'default_region': 'cn-beijing',
        'regions': [
            'cn-qingdao',
            'cn-beijing',
            'cn-chengdu',
            'cn-zhangjiakou',
            'cn-huhehaote',
            'cn-wulanchabu',
            'cn-hangzhou',
            'cn-shanghai',
            'cn-nanjing',
            'cn-fuzhou',
            'cn-shenzhen',
            'cn-heyuan',
            'cn-guangzhou',
            'cn-hongkong',

            'ap-southeast-1',
            'ap-southeast-2',
            'ap-southeast-3',
            'ap-southeast-5',
            'ap-southeast-6',
            'ap-southeast-7',
            'ap-south-1',
            'ap-northeast-1',
            'ap-northeast-2',
            'us-west-1',
            'us-east-1',
            'eu-central-1',
            'eu-west-1',
            'me-east-1'
        ]
    },
    'aws': {
        'default_region': 'cn-northwest-1',
        'regions': [
            'cn-northwest-1',
            'cn-north-1'
        ]
    }
}
