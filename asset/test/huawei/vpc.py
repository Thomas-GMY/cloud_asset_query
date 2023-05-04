# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0


from asset.test.base_test import BaseHuaweiTest
from asset.huawei.vpc import SecurityGroup


class TestSg(BaseHuaweiTest):
    def load_asset(self):
        return SecurityGroup(self.cred, region=self.region, dbconfig=self.db_config)