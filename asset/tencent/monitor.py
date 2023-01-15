# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import tencent_asset_register
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from asset.conf import today_zero_str, yesterday_zero_str

from tencentcloud.monitor.v20180724.monitor_client import MonitorClient, models

ccu_queries = {
    'NameSpace': 'QCE/CVM',
    'MetricName': 'CPUUsage',
    'Period': '3600',
    'Instances': [],
    'StartTime': yesterday_zero_str,
    'EndTime': 'QCE/CVM',
}
cvm_ccu_asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'MetricName', 'type': 'str', 'len': 16},
    {'name': 'Period', 'type': 'int'},
    {'name': 'Timestamps', 'type': 'datetime'},
    {'name': 'value', 'type': 'float'}
]


@tencent_asset_register.register('cvm_cpu_usage')
class CvmCpuUsage(TencentAsset):
    _des_request_func = 'GetMonitorData'
    _des_request = models.GetMonitorDataRequest()
    _response_field = 'Response'

    _table_name = 'tencent_cmv_cpu_usage'
    _asset_columns = []
    _table_args = (UniqueConstraint('account_id', 'timestamps', 'instance_id', name='tencent_instance_ccu'))

    def _get_client(self):
        return MonitorClient(self.cred, self.region)

    def _paginate_all_assets(self):
        """初始化self._des_request的参数↓"""
        for key, value in ccu_queries.items():
            setattr(self._des_request, key, value)

        from asset.tencent.cvm import Cvm
        assets = []
        instances = Cvm(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
        pagesize = 50

        for index in range(len(instances) // pagesize + 1):
            _instances = instances[index * pagesize: index * pagesize + pagesize]
            if not _instances:
                continue
            self._des_request.Instances = [
                {'Dimensions': [{'Name': 'InstanceId', 'Value': _instance['InstanceId']}]} for _instance in _instances]
            response = self._describe(
                self.client, self._des_request_func, self._des_request, self._response_field).parser_response()
            print(response)





