# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseTencentTest
from asset.tencent.cvm import Cvm


class TestCvn(BaseTencentTest):
    def load_asset(self):
        return Cvm(self.cred, self.region, dbconfig=self.db_config)
