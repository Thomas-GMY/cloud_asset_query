# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import click

from yaml import load, Loader

from asset.commands import Fetch
from asset.schema import DbConfig
from asset.utils import register_assets
from asset.conf import PROVIDERS, REGIONS, PROVIDER_PROFILES
from asset.exceptions import BaseCloudAssetException


@click.group()
def main():
    pass


@click.command()
@click.option('--cloud-provider', help=f'support cloud providers {PROVIDERS}', type=str)
@click.option('--profile-path', help='', type=str)
@click.option('--assets', help='', type=str)
@click.option('--regions', help='', type=str)
@click.option('--log-dir-path', help='', type=str)
def fetch(cloud_provider, profile_path, assets, regions=None, log_dir_path='./'):
    if cloud_provider not in PROVIDERS:
        raise BaseCloudAssetException(f'not support {cloud_provider}, only support cloud providers {PROVIDERS}')

    if not os.path.exists(profile_path):
        raise BaseCloudAssetException(f'not find the profile`s file by {profile_path}')

    if assets is None:
        raise BaseCloudAssetException('assets not be None!')

    with open(profile_path, 'r') as f:
        profile = load(f, Loader=Loader)

    dbconfig = profile.get('dbconfig', None)
    if dbconfig is None:
        dbconfig = DbConfig()
    else:
        dbconfig = DbConfig(**profile.pop('dbconfig'))

    cloud_providers = profile.get('cloud_providers', None)
    if cloud_providers is None:
        raise BaseCloudAssetException('cloud_providers not be None')
    cloud_provider_profile = filter(lambda x: x['cloud_provider'] == cloud_provider, cloud_providers).__next__()

    _regions = cloud_provider_profile.pop('regions')
    if regions is None:
        regions = _regions if _regions else REGIONS[cloud_provider]['default_region'].split(',')
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

    if assets == 'all':
        assets = 'all'
    else:
        assets = set(assets.split(','))
        if not assets:
            raise BaseCloudAssetException(f'not find assets: {assets}')
        diff_assets = assets.difference(set(list(register_assets(cloud_provider=cloud_provider).keys())))
        if diff_assets:
            raise BaseCloudAssetException(f'not find {cloud_provider}`assets: {diff_assets}')
        assets = list(assets)

    cloud_provider_profile = PROVIDER_PROFILES[cloud_provider](**cloud_provider_profile)

    Fetch(cloud_provider, cloud_provider_profile, assets, regions, log_dir_path=log_dir_path, dbconfig=dbconfig).fetch()


main.add_command(fetch)


if __name__ == '__main__':
    main()
