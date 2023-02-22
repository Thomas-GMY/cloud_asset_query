# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseTencentTest
from asset.tencent.clb import Clb


class TestClb(BaseTencentTest):
    def load_asset(self):
        return Clb(self.cred, self.region, dbconfig=self.db_config)