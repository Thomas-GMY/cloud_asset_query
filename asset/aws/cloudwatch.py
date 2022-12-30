# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import aws_asset_register
from asset.base import AwsAsset, AssetColumn, UniqueConstraint


ecu_asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'Timestamp', 'type': 'str', 'len': 64},
    {'name': 'Maximum', 'type': 'decimal'},
    {'name': 'Unit', 'type': 'str', 'len': 16}
]


@aws_asset_register.register('ec2_cpu_utilization')
class Ec2CpuUtilization(AwsAsset):
    _asset_name = 'cloudwatch'
    _des_request = 'get_metric_statistics'
    _response_field = 'Datapoints'

    _table_name = 'aws_ec2_cpu_utilization'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ecu_asset_columns]

    def _paginate_all_assets(self) -> list:
        """get_ec2_ids"""
        from asset.aws.ec2 import Ec2
        instances = Ec2(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
