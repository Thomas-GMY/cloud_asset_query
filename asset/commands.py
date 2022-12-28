# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import os
import json
import logging

from tencentcloud.common.credential import STSAssumeRoleCredential
from aliyunsdkcore.auth.credentials import RamRoleArnCredential

from asset.asset_register import tencent_asset_register, aliyun_asset_register
from asset.schema import DbConfig, TencentProfile, AliyunProfile
from asset.ctx import FetchCtx

from typing import Union


logger = logging.getLogger('cloud-asset-fetch')


def __register_assets():
    from asset import tencent
    from asset import aliyun


# register assets
__register_assets()


_default_output_dir = './'


class Fetch:
    _platform = ''
    logger = None

    def __init__(
            self,
            assets: list = None,
            profile: Union[TencentProfile, AliyunProfile] = None,
            dbconfig: DbConfig = DbConfig(),
            output_dir: str = _default_output_dir
    ):
        self.assets = assets
        self.profile = profile
        self.dbconfig = dbconfig
        self.output_dir = output_dir

        self._setup_logger()
        self._init_dbconfig()

    def fetch(self):
        raise NotImplementedError('')

    def _setup_logger(self):
        dir_path = os.path.join(self.output_dir, 'fetch')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        handler = logging.FileHandler(os.path.join(dir_path, 'fetch.log'))
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s:%(levelname)s:%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def _get_log_handle(self):
        dir_path = os.path.join(self.output_dir, 'fetch')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        handler = logging.FileHandler(os.path.join(dir_path, 'fetch.log'))
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s:%(levelname)s:%(message)s"))
        return handler

    def _init_dbconfig(self):
        from conf import CLOUD_ASSERT_DB
        CLOUD_ASSERT_DB.update(**self.dbconfig.dict())

    @property
    def support_assets(self):
        return self._support_assets()

    def _support_assets(self):
        pass

    @property
    def support_regions(self):
        return self._support_assets()

    def _support_regions(self):
        pass


class FetchTencent(Fetch):
    _platform = 'tencent'
    logger = logging.getLogger(f'{_platform}-cloud-asset-fetch')

    def __init__(
            self,
            assets: list = None,
            profile: TencentProfile = None,
            dbconfig: DbConfig = DbConfig(),
            output_dir: str = _default_output_dir
    ):
        super(FetchTencent, self).__init__(assets, profile, dbconfig, output_dir)
        _asset = tencent_asset_register.assets
        if assets:
            # self.assets = (tencent_asset_register.assets[asset] for asset in assets)
            self.assets = {asset: _asset.assets[asset] for asset in assets if asset in _asset.assets}
        else:
            self.assets = _asset
        self._ak = profile.ak
        self._sk = profile.sk
        self._roles = profile.roles
        self.dbconfig = dbconfig

    def fetch(self):
        with FetchCtx(self):
            for name, asset in self.assets.items():
                for role in self._roles:
                    cred = STSAssumeRoleCredential(
                        self._ak, self._sk, role.arn, role.session_name, role.duration_seconds)
                    for region in role.regions:

                        log_info = f'asset: {name}---region: {region}---role: {role.arn}'
                        try:
                            self.logger.info(f'{log_info}-fetch start')
                            asset(cred, region=region, dbconfig=self.dbconfig).fetch()
                            self.logger.info(f'{log_info}-fetch success')

                        except Exception as e:
                            self.logger.error(f'{log_info} fetch fail, error: {e}')
                            continue

    def _support_assets(self):
        return list(tencent_asset_register.assets.keys())

    def _support_regions(self):
        from conf import TENCENT_REGIONS
        return json.dumps(TENCENT_REGIONS, indent=4)


class FetchAliyun(Fetch):
    _platform = 'aliyun'
    logger = logging.getLogger(f'{_platform}-cloud-asset-fetch')

    def __init__(
            self,
            assets: list = None,
            profile: AliyunProfile = None,
            dbconfig: DbConfig = DbConfig(),
            output_dir: str = _default_output_dir
    ):
        super(FetchAliyun, self).__init__(assets, profile, dbconfig, output_dir)
        _asset = aliyun_asset_register.assets
        if assets:
            self.assets = {asset: _asset.assets[asset] for asset in assets if asset in _asset.assets}
        else:
            self.assets = _asset
        self._ak = profile.ak
        self._sk = profile.sk
        self._roles = profile.roles
        self.dbconfig = dbconfig

    def fetch(self):
        with FetchCtx(self):
            for name, asset in self.assets.items():
                for role in self._roles:
                    cred = RamRoleArnCredential(self._ak, self._sk, role.arn, role.session_name)

                    for region in role.regions:
                        log_info = f'asset: {name}---region: {region}---role: {role.arn}'
                        try:
                            self.logger.info(f'{log_info}-fetch start')
                            asset(cred, region=region, dbconfig=self.dbconfig).fetch()
                            self.logger.info(f'{log_info}-fetch success')

                        except Exception as e:
                            self.logger.error(f'{log_info} fetch fail, error: {e}')
                            continue

    def _support_assets(self):
        return list(aliyun_asset_register.assets.keys())

    def _support_regions(self):
        from conf import ALIYUN_REGIONS
        return json.dumps(ALIYUN_REGIONS, indent=4)





