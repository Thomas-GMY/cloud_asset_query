# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import logging
import importlib

from asset.asset_register import cloud_providers
from asset.schema import DbConfig, TencentProfile, AliyunProfile, AwsProfile, HuaweiProfile
from asset.ctx import FetchCtx

from typing import Union
from logging.handlers import TimedRotatingFileHandler


_default_log_dir_path = './'


class Fetch:
    logger = logging.getLogger('cloud-asset-fetch')

    def __init__(
            self,
            cloud_provider,
            profile: Union[TencentProfile, AliyunProfile, AwsProfile, HuaweiProfile],
            assets: Union[list, str],
            regions,
            log_dir_path=_default_log_dir_path,
            dbconfig=DbConfig()
    ):
        self.cloud_provider = cloud_provider
        self._register_assets = self.register_assets(cloud_provider=self.cloud_provider).assets  # type: dict

        self.profile = profile
        self.assets = list(self._register_assets.keys()) if assets == 'all' else assets
        self.regions = regions
        self.log_dir_path = log_dir_path
        self.dbconfig = dbconfig

        self._setup_logger()

    def fetch(self):
        with FetchCtx(self):
            for asset_name in self.assets:
                asset_obj = self._register_assets[asset_name]
                for cred in asset_obj.load_creds(self.profile):
                    for region in self.regions:
                        try:
                            asset = asset_obj(cred, region=region, dbconfig=self.dbconfig)
                            self.logger.info(
                                f'asset: {asset_name} ----region: {region} ----account_id: {asset.account_id}----start')
                            asset.fetch()
                        except Exception as e:
                            import traceback
                            self.logger.info(
                                f'asset: {asset_name} ----region: {region} ----account_id: {asset.account_id}----fail----error: {traceback.format_exc()}'
                            )
                            continue
                        self.logger.info(
                            f'asset: {asset_name} ----region: {region} ----account_id: {asset.account_id}----end')

    @classmethod
    def register_assets(cls, cloud_provider):
        importlib.import_module(f'asset.{cloud_provider}')
        return getattr(cloud_providers, cloud_provider)

    def _setup_logger(self):
        dir_path = os.path.join(self.log_dir_path, 'fetch_log')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(dir_path, 'fetch.log'), when="MIDNIGHT", interval=1, backupCount=7, encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s:%(levelname)s:%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)



