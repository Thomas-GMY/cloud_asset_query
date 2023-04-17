# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AliyunAsset, AssetColumn, UniqueConstraint
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeEipAddressesRequest import DescribeEipAddressesRequest
from aliyunsdkecs.request.v20140526.DescribeNatGatewaysRequest import DescribeNatGatewaysRequest
from aliyunsdkecs.request.v20140526.DescribeNetworkInterfacesRequest import DescribeNetworkInterfacesRequest


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
eip_asset_columns = [
    {'name': 'ReservationActiveTime', 'type': 'str'},
    {'name': 'Status', 'type': 'str'},
    {'name': 'ReservationOrderType', 'type': 'str'},
    {'name': 'AllocationTime', 'type': 'str'},
    {'name': 'Netmode', 'type': 'str'},
    {'name': 'ChargeType', 'type': 'str'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'SegmentInstanceId', 'type': 'str'},
    {'name': 'ReservationInternetChargeType', 'type': 'str'},
    {'name': 'BandwidthPackageId', 'type': 'str'},
    {'name': 'IpAddress', 'type': 'str'},
    {'name': 'Bandwidth', 'type': 'str'},
    {'name': 'ReservationBandwidth', 'type': 'str'},
    {'name': 'EipBandwidth', 'type': 'str'},
    {'name': 'Name', 'type': 'str'},
    {'name': 'InstanceRegionId', 'type': 'str'},
    {'name': 'DeletionProtection', 'type': 'str'},
    {'name': 'InstanceId', 'type': 'str'},
    {'name': 'SecondLimited', 'type': 'str'},
    {'name': 'InstanceType', 'type': 'str'},
    {'name': 'HDMonitorStatus', 'type': 'str'},
    {'name': 'RegionId', 'type': 'str'},
    {'name': 'BandwidthPackageBandwidth', 'type': 'str'},
    {'name': 'ServiceManaged', 'type': 'int'},
    {'name': 'ExpiredTime', 'type': 'str'},
    {'name': 'ResourceGroupId', 'type': 'str'},
    {'name': 'AllocationId', 'type': 'str'},
    {'name': 'InternetChargeType', 'type': 'str'},
    {'name': 'BusinessStatus', 'type': 'str'},
    {'name': 'BandwidthPackageType', 'type': 'str'},
    {'name': 'HasReservationData', 'type': 'str'},
    {'name': 'ISP', 'type': 'str'},
    {'name': 'OperationLocks', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'SecurityProtectionTypes', 'type': 'dict'},
    {'name': 'PublicIpAddressPoolId', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'Zone', 'type': 'str'}
]
nat_asset_columns = [
    {'name': 'Status', 'type': 'str'},
    {'name': 'CreationTime', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'Spec', 'type': 'str'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'NatGatewayId', 'type': 'str'},
    {'name': 'BusinessStatus', 'type': 'str'},
    {'name': 'Name', 'type': 'str'},
    {'name': 'InstanceChargeType', 'type': 'str'},
    {'name': 'RegionId', 'type': 'str'},
    {'name': 'ForwardTableIds', 'type': 'dict'},
    {'name': 'BandwidthPackageIds', 'type': 'dict'}
]
network_interface_columns = [
    {'name': 'CreationTime', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'Type', 'type': 'str'},
    {'name': 'Status', 'type': 'str'},
    {'name': 'NetworkInterfaceTrafficMode', 'type': 'str'},
    {'name': 'NetworkInterfaceName', 'type': 'str'},
    {'name': 'MacAddress', 'type': 'str'},
    {'name': 'QueuePairNumber', 'type': 'int'},
    {'name': 'NetworkInterfaceId', 'type': 'str'},
    {'name': 'ServiceID', 'type': 'str'},
    {'name': 'InstanceId', 'type': 'str'},
    {'name': 'OwnerId', 'type': 'str'},
    {'name': 'ServiceManaged', 'type': 'str'},
    {'name': 'VSwitchId', 'type': 'str'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'ResourceGroupId', 'type': 'str'},
    {'name': 'ZoneId', 'type': 'str'},
    {'name': 'PrivateIpAddress', 'type': 'str'},
    {'name': 'QueueNumber', 'type': 'int'},
    {'name': 'PrivateIpSets', 'type': 'dict'},
    {'name': 'Ipv6Sets', 'type': 'dict'},
    {'name': 'Ipv4PrefixSets', 'type': 'dict'},
    {'name': 'Ipv6PrefixSets', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'SecurityGroupIds', 'type': 'dict'},
    {'name': 'AssociatedPublicIp', 'type': 'dict'},
    {'name': 'Attachment', 'type': 'dict'}
]

ecs_field_document = 'https://help.aliyun.com/document_detail/25506.html?spm=a2c4g.11186623.0.0.3ac56cf0qyfOQ7#resultMapping'
eip_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeEipAddresses#workbench-doc-params'
nat_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeNatGateways#workbench-doc-response'
network_interface_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeNetworkInterfaces'


@cloud_providers.aliyun.register('ecs')
class Ecs(AliyunAsset):
    _des_request = DescribeInstancesRequest
    _response_field = 'Instances'
    _child_response_filed = 'Instance'

    _table_name = 'aliyun_ecs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='aliyun_instance'),)
    _field_document = ecs_field_document

    def _get_client(self):
        return AcsClient(credential=self.cred, region_id=self.region)


@cloud_providers.aliyun.register('eip')
class Eip(Ecs):
    _des_request = DescribeEipAddressesRequest
    _response_field = 'EipAddresses'
    _child_response_filed = 'EipAddress'

    _table_name = 'aliyun_eips'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in eip_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'ip_address', name='aliyun_uc_eip'),)
    _field_document = eip_field_document


@cloud_providers.aliyun.register('nat_gateway')
class NatGateway(Ecs):
    _des_request = DescribeNatGatewaysRequest
    _response_field = 'NatGateways'
    _child_response_filed = 'NatGateway'

    _table_name = 'aliyun_nat_gateway'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in nat_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'nat_gateway_id', name='aliyun_uc_ng'),)
    _field_document = eip_field_document


@cloud_providers.aliyun.register('network_interface')
class NetworkInterface(Ecs):
    _des_request = DescribeNetworkInterfacesRequest
    _response_field = 'NetworkInterfaceSets'
    _child_response_filed = 'NetworkInterfaceSet'

    _table_name = 'aliyun_network_interface'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in network_interface_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'network_interface_id', name='aliyun_uc_nii'),)
    _field_document = network_interface_field_document
