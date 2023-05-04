# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aliyun.ecs import Ecs, Eip, NatGateway, NetworkInterface, Disk, Sg
from asset.test.base_test import BaseAliyunTest


class TestEcs(BaseAliyunTest):
    def load_asset(self):
        return Ecs(self.cred, self.region, self.db_config)


class TestNat(BaseAliyunTest):
    def load_asset(self):
        return NatGateway(self.cred, self.region, self.db_config)


class TestNetworkInterface(BaseAliyunTest):
    def load_asset(self):
        return NetworkInterface(self.cred, self.region, self.db_config)


class TestEip(BaseAliyunTest):
    def load_asset(self):
        return Eip(self.cred, self.region, self.db_config)


class TestDisk(BaseAliyunTest):
    def load_asset(self):
        return Disk(self.cred, self.region, self.db_config)


class TestSg(BaseAliyunTest):
    def load_asset(self):
        return Sg(self.cred, self.region, self.db_config)


