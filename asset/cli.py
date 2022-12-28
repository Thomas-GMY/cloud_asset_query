# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import json
import click

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from asset.commands import FetchTencent, FetchAliyun
from asset.schema import TencentProfile, AliyunProfile, DbConfig


@click.group()
def main():
    pass


@click.command()
@click.option('--config', help='', type=str)
def fetch(config):

    with open(config, 'r') as fp:
        config = json.loads(fp.read())

    dbconfig, assets_config, output_dir = DbConfig(**config['dbconfig']), config['assets_config'], config['output_dir']
    for asset_config in assets_config:
        platform = asset_config['platform']
        assets = asset_config['assets']
        profile = asset_config['profile']

        if platform == 'tencent':
            FetchTencent(assets, profile=TencentProfile(**profile), dbconfig=dbconfig, output_dir=output_dir).fetch()
        elif platform == 'aliyun':
            FetchAliyun(assets, profile=AliyunProfile(**profile), dbconfig=dbconfig, output_dir=output_dir).fetch()
        else:
            raise ValueError(f'not support platform: {platform}')


main.add_command(fetch)


if __name__ == '__main__':
    main()
