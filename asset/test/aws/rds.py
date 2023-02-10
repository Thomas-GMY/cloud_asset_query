# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.rds import DbInstances, DbClusters


# class TestDbInstances(BaseAwsTest):
#
#     def load_asset(self):
#         return DbInstances(self.cred, self.region, dbconfig=self.db_config)


class TestDbClusters(BaseAwsTest):

    def load_asset(self):
        return DbClusters(self.cred, self.region, dbconfig=self.db_config)