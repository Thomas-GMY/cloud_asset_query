# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

class BaseCloudAssetException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'BaseCloudAssetException: [{self.msg}]'
