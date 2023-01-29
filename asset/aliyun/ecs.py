# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AliyunAsset, AssetColumn, UniqueConstraint
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


asset_columns = [
    {'name': 'CreationTime', 'type': 'str', 'len': 64},
    {'name': 'SerialNumber', 'type': 'str', 'len': 128},
    {'name': 'Status', 'type': 'str', 'len': 16},
    {'name': 'DeploymentSetId', 'type': 'str', 'len': 128},
    {'name': 'KeyPairName', 'type': 'str', 'len': 128},
    {'name': 'SpotStrategy', 'type': 'str', 'len': 32},
    {'name': 'DeviceAvailable', 'type': 'bool'},
    {'name': 'LocalStorageCapacity', 'type': 'float'},
    {'name': 'Description', 'type': 'str', 'len': 256},
    {'name': 'SpotDuration', 'type': 'int'},
    {'name': 'InstanceNetworkType', 'type': 'str', 'len': 16},
    {'name': 'InstanceName', 'type': 'str', 'len': 64},
    {'name': 'OSNameEn', 'type': 'str', 'len': 32},
    {'name': 'HpcClusterId', 'type': 'str', 'len': 128},
    {'name': 'SpotPriceLimit', 'type': 'float'},
    {'name': 'Memory', 'type': 'int', 'len': 128},
    {'name': 'OSName', 'type': 'str', 'len': 32},
    {'name': 'DeploymentSetGroupNo', 'type': 'int'},
    {'name': 'ImageId', 'type': 'str', 'len': 128},
    {'name': 'GPUSpec', 'type': 'str', 'len': 64},
    {'name': 'AutoReleaseTime', 'type': 'str', 'len': 64},
    {'name': 'DeletionProtection', 'type': 'bool'},
    {'name': 'StoppedMode', 'type': 'str', 'len': 16},
    {'name': 'GPUAmount', 'type': 'int'},
    {'name': 'HostName', 'type': 'str', 'len': 128},
    {'name': 'InstanceId', 'type': 'str', 'len': 128},
    {'name': 'InternetMaxBandwidthOut', 'type': 'int'},
    {'name': 'InternetMaxBandwidthIn', 'type': 'int'},
    {'name': 'InstanceType', 'type': 'str', 'len': 64},
    {'name': 'InstanceChargeType', 'type': 'str', 'len': 32},
    {'name': 'RegionId', 'type': 'str', 'len': 16},
    {'name': 'IoOptimized', 'type': 'bool'},
    {'name': 'StartTime', 'type': 'str', 'len': 64},
    {'name': 'Cpu', 'type': 'int'},
    {'name': 'LocalStorageAmount', 'type': 'int'},
    {'name': 'ExpiredTime', 'type': 'str', 'len': 64},
    {'name': 'ResourceGroupId', 'type': 'str', 'len': 128},
    {'name': 'InternetChargeType', 'type': 'str', 'len': 32},
    {'name': 'ZoneId', 'type': 'str', 'len': 32},
    {'name': 'Recyclable', 'type': 'bool'},
    {'name': 'CreditSpecification', 'type': 'str', 'len': 16},
    {'name': 'InstanceTypeFamily', 'type': 'str', 'len': 16},
    {'name': 'OSType', 'type': 'str', 'len': 8},
    {'name': 'NetworkInterfaces', 'type': 'dict'},
    {'name': 'OperationLocks', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'RdmaIpAddress', 'type': 'dict'},
    {'name': 'SecurityGroupIds', 'type': 'dict'},
    {'name': 'PublicIpAddress', 'type': 'dict'},
    {'name': 'InnerIpAddress', 'type': 'dict'},
    {'name': 'VpcAttributes', 'type': 'dict'},
    {'name': 'EipAddress', 'type': 'dict'},
    {'name': 'HibernationOptions', 'type': 'dict'},
    {'name': 'DedicatedHostAttribute', 'type': 'dict'},
    {'name': 'EcsCapacityReservationAttr', 'type': 'dict'},
    {'name': 'DedicatedInstanceAttribute', 'type': 'dict'},
    {'name': 'CpuOptions', 'type': 'dict'},
    {'name': 'MetadataOptions', 'type': 'dict'},
    {'name': 'ImageOptions', 'type': 'dict'}
]


@cloud_providers.aliyun.register('acs')
class Ecs(AliyunAsset):
    _des_request = DescribeInstancesRequest()
    _response_field = 'Instances'
    _child_response_filed = 'Instance'

    _table_name = 'aliyun_ecs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='aliyun_instance'),)

    def _get_client(self):
        return AcsClient(credential=self.cred, region_id=self.region)
