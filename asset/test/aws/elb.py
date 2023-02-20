# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.elb import Elb


class TestElb(BaseAwsTest):

    def load_asset(self):
        return Elb(self.cred, self.region, dbconfig=self.db_config)
