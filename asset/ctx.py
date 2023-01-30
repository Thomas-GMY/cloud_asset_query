# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import time


class FetchCtx:
    def __init__(self, fetch):
        self.fetch = fetch
        self.time_now = time.time()

    def __enter__(self):
        self.fetch.logger.info(f'-------{self.fetch.cloud_provider} fetch start -------')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fetch.logger.info(f'-------{self.fetch.cloud_provider} fetch end, spend time {time.time() - self.time_now}/s   -------')
