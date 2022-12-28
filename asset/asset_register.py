# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0


class AssetRegister:
    def __init__(self):
        self._assets = {}

    @property
    def assets(self) -> dict:
        return self._assets

    def register(self, name: str):
        def _register_class(asset):
            self._assets[name] = asset
            return asset
        return _register_class


class TencentAssetRegister(AssetRegister):
    pass


class AliyunAssetRegister(AssetRegister):
    pass


class AwsAssetRegister(AssetRegister):
    pass


tencent_asset_register = TencentAssetRegister()
aliyun_asset_register = AliyunAssetRegister()
aws_asset_register = AwsAssetRegister()





