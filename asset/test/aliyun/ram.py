# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aliyun.ram import User
from asset.test.base_test import BaseAliyunTest


class TestUser(BaseAliyunTest):
    def load_asset(self):
        return User(self.cred, self.region, self.db_config)
