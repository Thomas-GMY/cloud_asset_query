# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import json
import click

from asset.commands import FetchTencent, FetchAliyun
from asset.schema import DbConfig
from asset.utils import register_assets
from asset.conf import PROVIDERS, PROVIDER_PROFILES, REGIONS
from asset.exceptions import BaseCloudAssetException


@click.group()
def main():
    pass


@click.command()
@click.option('--cloud-provider', help=f'support cloud providers {PROVIDERS}', type=str)
@click.option('--profile-path', help='', type=str)
@click.option('--assets', help='', type=str)
@click.option('--regions', help='', type=str)
@click.option('--dbconfig-path', help='', type=str)
@click.option('--log-dir-path', help='', type=str, default='./')
def fetch(cloud_provider, profile_path, assets, regions=None, dbconfig_path=None):
    if cloud_provider not in PROVIDERS:
        raise BaseCloudAssetException(f'not support {cloud_provider}, only support cloud providers {PROVIDERS}')

    if not os.path.exists(profile_path):
        raise BaseCloudAssetException(f'not find the profile`s file by {profile_path}')
    else:
        with open(profile_path, 'r') as fp:
            profile = PROVIDER_PROFILES[cloud_provider](**json.load(fp))

    assets = set(assets.split(','))
    if not assets:
        raise BaseCloudAssetException(f'not find assets: {assets}')
    diff_assets = assets.difference(set(list(register_assets(cloud_provider=cloud_provider).keys())))
    if diff_assets:
        raise BaseCloudAssetException(f'not find {cloud_provider}`assets: {diff_assets}')
    assets = list(assets)

    if regions is None:
        regions = REGIONS[cloud_provider]['default_region'].split(',')
    else:
        cloud_regions = REGIONS[cloud_provider]['regions']
        if regions == 'all':
            regions = cloud_regions
        else:
            regions = set(regions.split(','))
            diff_regions = regions.difference(cloud_regions)
            if diff_regions:
                raise BaseCloudAssetException(f'not support regions: {regions}, just support: {cloud_regions}')
            regions = list(regions)

    if os.path.exists(dbconfig_path):
        with open(dbconfig_path, 'r') as fp:
            dbconfig = DbConfig(**json.load(fp))
    else:
        dbconfig = DbConfig()

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
