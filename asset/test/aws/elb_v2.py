# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.elb_v2 import ElbV2, ElbV2Listeners, ElbV2TargetGroups, ElbV2TargetGroupHealth


class TestElbV2(BaseAwsTest):

    def load_asset(self):
        return ElbV2(self.cred, self.region, dbconfig=self.db_config)


class TestElbV2Listeners(BaseAwsTest):

    def load_asset(self):
        return ElbV2Listeners(self.cred, self.region, dbconfig=self.db_config)


class TestElbV2TargetGroups(BaseAwsTest):

    def load_asset(self):
        return ElbV2TargetGroups(self.cred, self.region, dbconfig=self.db_config)


class TestElbV2TargetGroupHealth(BaseAwsTest):

    def load_asset(self):
        return ElbV2TargetGroupHealth(self.cred, self.region, dbconfig=self.db_config)
