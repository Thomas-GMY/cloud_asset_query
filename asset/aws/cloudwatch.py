# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import arrow
import datetime
from asset.asset_register import aws_asset_register
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

yesterday_start = arrow.now().shift(days=-3).datetime.date().strftime('%Y-%m-%d 00:00:00')
yesterday_end = arrow.now().shift(days=-3).datetime.date().strftime('%Y-%m-%d 23:59:59')
ecu_asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'Timestamp', 'type': 'str', 'len': 64},
    {'name': 'Maximum', 'type': 'decimal'},
    {'name': 'Unit', 'type': 'str', 'len': 16}
]
ecu_field_document = ''


@aws_asset_register.register('ec2_cpu_utilization')
class Ec2CpuUtilization(AwsAsset):
    _asset_name = 'cloudwatch'
    _des_request = 'get_metric_data'
    _response_field = 'Datapoints'
    _des_request_kwargs: dict = {
        'MetricDataQueries': [
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': []
                    },
                    'Period': 3600,
                    'Stat': 'Minimum',
                    'Unit': 'Seconds'
                }
            }
        ],
        'StartTime': datetime.datetime(2023, 1, 7),
        'EndTime': datetime.datetime(2023, 1, 8)
    }
    _field_document = ecu_field_document

    _table_name = 'aws_ec2_cpu_utilization'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ecu_asset_columns]

    def _paginate_all_assets(self) -> list:
        """get_ec2_ids"""
        from asset.aws.ec2 import Ec2
        instances = Ec2(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
        pagesize = 20
        for index in range(len(instances) // pagesize + 1):
            _instances = instances[index * pagesize: index * pagesize + pagesize]
            if not _instances:
                continue
            _instances = [{'Name': 'InstanceId', 'Value': instance['InstanceId']} for instance in _instances]
            self._des_request_kwargs['MetricDataQueries'][0]['MetricStat']['Metric']['Dimensions'] = [{'Name': 'InstanceId', 'Value': 'i-0bf03669fc5c6da52'}]
            _assets, _ = self._describe(
                self.client,
                self._des_request,
                self._response_field,
                self._child_response_filed,
                des_request_kwargs=self._des_request_kwargs,
                parser_response_func=self.parser_response
            ).parser_response()
            print(_assets)
