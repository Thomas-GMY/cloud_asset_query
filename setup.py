# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup


packages = [
    'asset',
    'asset.aliyun',
    'asset.tencent',
    'asset.aws',
    'asset.huawei'
]
install_requires = [
    'tencentcloud-sdk-python==3.0.898',

    'aliyun-python-sdk-core==2.13.36',
    'aliyun-python-sdk-ecs==4.24.26',
    'aliyun-python-sdk-sts==3.1.0',
    'aliyun-python-sdk-ram==3.3.0',

    'boto3==1.26.29',

    'huaweicloudsdkcore==3.1.37',
    'huaweicloudsdkecs==3.1.37',
    'huaweicloudsdkiam==3.1.37',
    'huaweicloudsdkevs==3.1.37',
    'huaweicloudsdkeip==3.1.37',
    'huaweicloudsdknat==3.1.37',
    'huaweicloudsdkelb==3.1.37',
    'huaweicloudsdkvpc==3.1.37',
    'esdk-obs-python==3.22.2',

    'SQLAlchemy==1.4.44',
    'psycopg2==2.9.5',
    'click==8.1.3',
    'pydantic==1.10.2',
    'requests==2.28.0',
    'pyyaml==6.0',
    'arrow==1.2.3'
]
entry_points = {'console_scripts': ['cloud-asset = asset.cli:main']}
setup_kwargs = {
    'name': 'cloud-asset',
    'version': '0.0.4.5',
    'description': 'Cloud Asset - Asset For Postgres',
    'license': 'Apache-2.0',
    'long_description': '',
    'long_description_content_type': 'text/markdown',
    'author': 'Cloud Asset Authors',
    'author_email': '',
    'packages': packages,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}

setup(**setup_kwargs)
