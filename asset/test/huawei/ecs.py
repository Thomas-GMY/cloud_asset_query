# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseHuaweiTest
from asset.huawei.ecs import Ecs, Eip, Nat, Evs


class TestEcs(BaseHuaweiTest):

    def load_asset(self):
        return Ecs(self.cred, region=self.region, dbconfig=self.db_config)


class TestEip(BaseHuaweiTest):

    def load_asset(self):
        return Eip(self.cred, region=self.region, dbconfig=self.db_config)


class TestNat(BaseHuaweiTest):

    def load_asset(self):
        return Nat(self.cred, region=self.region, dbconfig=self.db_config)


class TestEvs(BaseHuaweiTest):

    def load_asset(self):
        return Evs(self.cred, region=self.region, dbconfig=self.db_config)
