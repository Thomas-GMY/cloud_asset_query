# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from tencentcloud.cvm.v20170312.cvm_client import CvmClient, models

asset_columns = [
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'Placement', 'type': 'dict'},
    {'name': 'InstanceType', 'type': 'str', 'len': 16},
    {'name': 'CPU', 'type': 'int'},
    {'name': 'Memory', 'type': 'int'},
    {'name': 'RestrictState', 'type': 'str', 'len': 64},
    {'name': 'InstanceName', 'type': 'str', 'len': 64},
    {'name': 'InstanceChargeType', 'type': 'str', 'len': 64},
    {'name': 'SystemDisk', 'type': 'dict'},
    {'name': 'DataDisks', 'type': 'dict'},
    {'name': 'PrivateIpAddresses', 'type': 'dict'},
    {'name': 'PublicIpAddresses', 'type': 'dict'},
    {'name': 'InternetAccessible', 'type': 'dict'},
    {'name': 'VirtualPrivateCloud', 'type': 'dict'},
    {'name': 'ImageId', 'type': 'str', 'len': 64},
    {'name': 'RenewFlag', 'type': 'str', 'len': 64},
    {'name': 'CreatedTime', 'type': 'str', 'len': 64},
    {'name': 'ExpiredTime', 'type': 'str', 'len': 64},
    {'name': 'OsName', 'type': 'str', 'len': 64},
    {'name': 'SecurityGroupIds', 'type': 'dict'},
    {'name': 'LoginSettings', 'type': 'dict'},
    {'name': 'InstanceState', 'type': 'str', 'len': 64},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'LicenseType', 'type': 'str', 'len': 64},
    {'name': 'CamRoleName', 'type': 'str', 'len': 128}
]

cvm_field_document = 'https://cloud.tencent.com/document/api/213/15728'


@cloud_providers.tencent.register('cvm')
class Cvm(TencentAsset):
    _des_request_func = 'DescribeInstances'
    _des_request = models.DescribeInstancesRequest()
    _response_field = 'InstanceSet'

    _table_name = 'tencent_cvm'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='tencent_instance'),)
    _field_document = cvm_field_document

    def _get_client(self):
        return CvmClient(self.cred, self.region)

