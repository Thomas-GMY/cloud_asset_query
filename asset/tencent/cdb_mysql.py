# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from tencentcloud.cdb.v20170320.cdb_client import CdbClient, models

cdb_m_asset_columns = [
    {'name': 'WanStatus', 'type': 'int'},
    {'name': 'Zone', 'type': 'str'},
    {'name': 'WanPort', 'type': 'int'},
    {'name': 'RoVipInfo', 'type': 'dict'},
    {'name': 'Memory', 'type': 'int'},
    {'name': 'EngineType', 'type': 'str'},
    {'name': 'Status', 'type': 'int'},
    {'name': 'VpcId', 'type': 'int'},
    {'name': 'SlaveInfo', 'type': 'dict'},
    {'name': 'InstanceId', 'type': 'str'},
    {'name': 'PhysicalId', 'type': 'str'},
    {'name': 'Volume', 'type': 'int'},
    {'name': 'AutoRenew', 'type': 'int'},
    {'name': 'ProtectMode', 'type': 'int'},
    {'name': 'CdbError', 'type': 'int'},
    {'name': 'DeviceClass', 'type': 'str'},
    {'name': 'MasterInfo', 'type': 'dict'},
    {'name': 'DeployGroupId', 'type': 'str'},
    {'name': 'InstanceNodes', 'type': 'int'},
    {'name': 'RoGroups', 'type': 'dict'},
    {'name': 'ProjectId', 'type': 'int'},
    {'name': 'DeadlineTime', 'type': 'str'},
    {'name': 'DeployMode', 'type': 'int'},
    {'name': 'TaskStatus', 'type': 'int'},
    {'name': 'SubnetId', 'type': 'int'},
    {'name': 'DeviceType', 'type': 'str'},
    {'name': 'EngineVersion', 'type': 'str'},
    {'name': 'MaxDelayTime', 'type': 'int'},
    {'name': 'InstanceName', 'type': 'str'},
    {'name': 'Cpu', 'type': 'int'},
    {'name': 'DrInfo', 'type': 'dict'},
    {'name': 'UniqVpcId', 'type': 'str'},
    {'name': 'WanDomain', 'type': 'str'},
    {'name': 'InitFlag', 'type': 'int'},
    {'name': 'PayType', 'type': 'int'},
    {'name': 'InstanceType', 'type': 'int'},
    {'name': 'Vip', 'type': 'str'},
    {'name': 'UniqSubnetId', 'type': 'str'},
    {'name': 'Qps', 'type': 'int'},
    {'name': 'Vport', 'type': 'int'},
    {'name': 'TagList', 'type': 'dict'},
    {'name': 'CreateTime', 'type': 'str'},
    {'name': 'ZoneId', 'type': 'int'},
    {'name': 'ZoneName', 'type': 'str'}
]

cdb_m_field_document = 'https://cloud.tencent.com/document/api/236/15872#1.-.E6.8E.A5.E5.8F.A3.E6.8F.8F.E8.BF.B0'


@cloud_providers.tencent.register('cdb_mysql')
class CdbMysql(TencentAsset):
    _des_request_func = 'DescribeDBInstances'
    _des_request = models.DescribeDBInstancesRequest()
    _response_field = 'Items'

    _table_name = 'tencent_cdb_mysql'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in cdb_m_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='tencent_uc_cdb_m'),)
    _field_document = cdb_m_field_document

    def _get_client(self):
        return CdbClient(self.cred, self.region)
