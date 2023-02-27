# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aliyun.ecs import Ecs
from asset.test.base_test import BaseAliyunTest


class TestEcs(BaseAliyunTest):
    def load_asset(self):
        return Ecs(self.cred, self.region, self.db_config)
