# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseTencentTest
from asset.tencent.cam import User, UserAk


class TestUser(BaseTencentTest):
    def load_asset(self):
        return User(self.cred, self.region, dbconfig=self.db_config)


class TestUserAk(BaseTencentTest):
    def load_asset(self):
        return UserAk(self.cred, self.region, dbconfig=self.db_config)