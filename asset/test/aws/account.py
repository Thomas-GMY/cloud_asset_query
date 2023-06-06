# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.test.base_test import BaseAwsTest
from asset.aws.account import ContactInformation, AlternateContact


class TestContactInformation(BaseAwsTest):

    def load_asset(self):
        return ContactInformation(self.cred, self.region, dbconfig=self.db_config)


# class TestAlternateContact(BaseAwsTest):
#
#     def load_asset(self):
#         return AlternateContact(self.cred, self.region, dbconfig=self.db_config)