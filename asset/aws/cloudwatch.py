# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import copy
import datetime
from asset.base import AwsAsset, AssetColumn, UniqueConstraint
from asset.asset_register import cloud_providers
from asset.conf import today, yesterday

ecu_asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'Metric', 'type': 'str', 'len': 16},
    {'name': 'MetricTimestamp', 'type': 'datetime'},
    {'name': 'MetricValue', 'type': 'float'},
    {'name': 'Period', 'type': 'int'}
]
period = 3600
ecu_metric_dq = [
    {
        'Id': 'm{instance_id}1',
        'Label': 'Minimum::{instance_id}',
        'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/EC2',
                'MetricName': 'CPUUtilization',
                'Dimensions': []
            },
            'Period': period,
            'Stat': 'Minimum'
        }
    },
    {
        'Id': 'm{instance_id}2',
        'Label': 'Maximum::{instance_id}',
        'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/EC2',
                'MetricName': 'CPUUtilization',
                'Dimensions': []
            },
            'Period': period,
            'Stat': 'Maximum'
        }
    }
]
ecu_field_document = ''


@cloud_providers.aws.register('ec2_cpu_utilization')
class Ec2CpuUtilization(AwsAsset):
    """
        get ec2_cpu_utilization metric, include (Minimum, Maximum)
    """
    _asset_name = 'cloudwatch'
    _des_request = 'get_metric_data'
    _response_field = 'MetricDataResults'
    _des_request_kwargs: dict = {
        'MetricDataQueries': [],
        'StartTime': datetime.datetime(yesterday.year, yesterday.month, yesterday.day),
        'EndTime': datetime.datetime(today.year, today.month, today.day)
    }
    _field_document = ecu_field_document

    _table_name = 'aws_ec2_cpu_utilization'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ecu_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'instance_id', 'metric', 'metric_timestamp', name='aws_uc_ec2_cpu_u'),)

    def _paginate_all_assets(self) -> list:
        from asset.aws.ec2 import Ec2
        assets = []
        instances = Ec2(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
        pagesize = 50

        for index in range(len(instances) // pagesize + 1):
            _instances = instances[index * pagesize: index * pagesize + pagesize]
            if not _instances:
                continue
            metric_data_queries = []
            for instance in _instances:
                instance_id = instance['InstanceId']
                instance_id_sp = instance_id.split('-')[1]
                dimension = [{'Name': 'InstanceId', 'Value': instance_id}]
                _ecu_metric_dq = copy.deepcopy(ecu_metric_dq)

                # metric: Minimum
                _ecu_metric_dq[0]['MetricStat']['Metric']['Dimensions'] = dimension
                _ecu_metric_dq[0]['Id'] = _ecu_metric_dq[0]['Id'].format(instance_id=instance_id_sp)
                _ecu_metric_dq[0]['Label'] = _ecu_metric_dq[0]['Label'].format(instance_id=instance_id_sp)

                # metric: Maximum
                _ecu_metric_dq[1]['MetricStat']['Metric']['Dimensions'] = dimension
                _ecu_metric_dq[1]['Id'] = _ecu_metric_dq[1]['Id'].format(instance_id=instance_id_sp)
                _ecu_metric_dq[1]['Label'] = _ecu_metric_dq[1]['Label'].format(instance_id=instance_id_sp)

                metric_data_queries += _ecu_metric_dq

            self._des_request_kwargs['MetricDataQueries'] = metric_data_queries
            result = self._describe(
                self.client,
                self._des_request,
                self._response_field,
                self._child_response_filed,
                des_request_kwargs=self._des_request_kwargs,
                parser_response_func=self.parser_response
            ).describe()
            metric_drs = result.get('MetricDataResults', [])
            for metric_dr in metric_drs:
                metric, instance_id = metric_dr['Label'].split('::')
                values = zip(metric_dr['Timestamps'], metric_dr['Values'])
                assets += [
                    {
                        'InstanceId': instance_id,
                        'Metric': metric,
                        'MetricTimestamp': value[0],
                        'MetricValue': value[1],
                        'Period': period
                    } for value in values
                ]
        return sorted(assets, key=lambda a: a['MetricTimestamp'])


