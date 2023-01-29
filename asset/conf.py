# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import arrow
from sqlalchemy import Integer, String, JSON, Date, Text, DateTime, NUMERIC, DECIMAL, FLOAT
from asset.schema import TencentRole, AliyunRole, AwsProfile


PROVIDERS = ('tencent', 'aliyun', 'aws')
PROVIDER_PROFILES = {
    'tencent': TencentRole,
    'aliyun': AliyunRole,
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
            'ap-singapore',
            'na-siliconvalley',
            'na-toronto'
        ]
    },
    'aliyun': {
        'default_region': 'cn-beijing',
        'regions': [
            'cn-qingdao',
            'cn-beijing'
        ]
    }
}