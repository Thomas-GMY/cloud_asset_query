# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0
import copy
import datetime
from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from asset.conf import today, yesterday

from tencentcloud.monitor.v20180724.monitor_client import MonitorClient, models

ccu_queries = {
    'Namespace': 'QCE/CVM',
    'MetricName': 'CPUUsage',
    'Period': 3600,
    'Instances': [],
    'StartTime': datetime.datetime(yesterday.year, yesterday.month, yesterday.day).isoformat() + '+08:00',
    'EndTime': datetime.datetime(today.year, today.month, today.day).isoformat() + '+08:00',
}
cvm_ccu_asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'MetricName', 'type': 'str', 'len': 16},
    {'name': 'Period', 'type': 'int'},
    {'name': 'Timestamp', 'type': 'datetime'},
    {'name': 'MetricValue', 'type': 'float'}
]

get_metric_field_document = 'https://cloud.tencent.com/document/api/248/31014'


@cloud_providers.tencent.register('cvm_cpu_usage')
class CvmCpuUsage(TencentAsset):
    _des_request_func = 'GetMonitorData'
    _des_request = models.GetMonitorDataRequest()
    _response_field = 'DataPoints'

    _table_name = 'tencent_cvm_cpu_usage'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in cvm_ccu_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'timestamp', 'instance_id', name='tencent_instance_ccu'), )
    _field_document = get_metric_field_document

    def _get_client(self):
        return MonitorClient(self.cred, self.region)

    def _paginate_all_assets(self):
        """初始化self._des_request的参数↓"""
        _des_request = copy.deepcopy(self._des_request)
        for key, value in ccu_queries.items():
            setattr(_des_request, key, value)

        from asset.tencent.cvm import Cvm
        assets = []
        instances = Cvm(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
        pagesize = 50

        for index in range(len(instances) // pagesize + 1):
            _instances = instances[index * pagesize: index * pagesize + pagesize]
            if not _instances:
                continue
            _des_request.Instances = [
                {'Dimensions': [{'Name': 'InstanceId', 'Value': _instance['InstanceId']}]} for _instance in _instances]
            results = self._describe(
                self.client, self._des_request_func, _des_request, self._response_field).parser_response()
            for result in results:
                count = 0
                for _time_stamp in result['Timestamps']:
                    assets.append(
                        {
                            'InstanceId': result['Dimensions'][0]['Value'],
                            'MetricName': 'CpuUsage',
                            'Period': 3600,
                            'Timestamp': datetime.datetime.fromtimestamp(_time_stamp),
                            'MetricValue': result['Values'][count]
                        }
                    )
                    count += 1

        return sorted(assets, key=lambda x: x['Timestamp'])





