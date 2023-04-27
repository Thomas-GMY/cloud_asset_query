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


class HuaweiRegister(AssetRegister):
    pass


class CloudProviders:
    tencent = TencentAssetRegister()
    aliyun = AliyunAssetRegister()
    aws = AwsAssetRegister()
    huawei = HuaweiRegister()


cloud_providers = CloudProviders()




