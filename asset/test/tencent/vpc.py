# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseTencentTest
from asset.tencent.vpc import Vpc, Subnet, RouteTable, Eip, NetworkInterfaces, Nat, SecurityGroups


class TestVpc(BaseTencentTest):
    def load_asset(self):
        return Vpc(self.cred, self.region, dbconfig=self.db_config)


class TestSubnet(BaseTencentTest):
    def load_asset(self):
        return Subnet(self.cred, self.region, dbconfig=self.db_config)


class TestRouteTable(BaseTencentTest):
    def load_asset(self):
        return RouteTable(self.cred, self.region, dbconfig=self.db_config)


class TestEip(BaseTencentTest):
    def load_asset(self):
        return Eip(self.cred, self.region, dbconfig=self.db_config)


class TestNetworkInterfaces(BaseTencentTest):
    def load_asset(self):
        return NetworkInterfaces(self.cred, self.region, dbconfig=self.db_config)


class TestNat(BaseTencentTest):
    def load_asset(self):
        return Nat(self.cred, self.region, dbconfig=self.db_config)


class TestSecurityGroups(BaseTencentTest):
    def load_asset(self):
        return SecurityGroups(self.cred, self.region, dbconfig=self.db_config)