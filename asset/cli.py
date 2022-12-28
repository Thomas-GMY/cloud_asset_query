# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import json
import click
import logging

from asset.commands import FetchTencent, FetchAliyun
from asset.schema import TencentProfile, AliyunProfile, DbConfig
from asset.conf import PLATFORMS


def __setup_logs(output_dir, platforms):
    dir_path = os.path.join(output_dir, platforms)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    aliyun_handle = logging.FileHandler(os.path.join(dir_path, 'fetch.log'))
    logging.basicConfig()


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
