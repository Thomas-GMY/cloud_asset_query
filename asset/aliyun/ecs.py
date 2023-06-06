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
from aliyunsdkecs.request.v20140526.DescribeDisksRequest import DescribeDisksRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupAttributeRequest import DescribeSecurityGroupAttributeRequest


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
disk_interface_columns = [
    {'name': 'SerialNumber', 'type': 'str'},
    {'name': 'CreationTime', 'type': 'str'},
    {'name': 'Status', 'type': 'str'},
    {'name': 'Type', 'type': 'str'},
    {'name': 'PerformanceLevel', 'type': 'str'},
    {'name': 'BdfId', 'type': 'str'},
    {'name': 'EnableAutoSnapshot', 'type': 'str'},
    {'name': 'StorageSetId', 'type': 'str'},
    {'name': 'StorageSetPartitionNumber', 'type': 'int'},
    {'name': 'DiskId', 'type': 'str'},
    {'name': 'DeleteAutoSnapshot', 'type': 'str'},
    {'name': 'StorageClusterId', 'type': 'str'},
    {'name': 'Encrypted', 'type': 'str'},
    {'name': 'IOPSRead', 'type': 'int'},
    {'name': 'MountInstanceNum', 'type': 'int'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'Device', 'type': 'str'},
    {'name': 'DiskName', 'type': 'str'},
    {'name': 'Portable', 'type': 'str'},
    {'name': 'ImageId', 'type': 'str'},
    {'name': 'KMSKeyId', 'type': 'str'},
    {'name': 'DeleteWithInstance', 'type': 'str'},
    {'name': 'DetachedTime', 'type': 'str'},
    {'name': 'SourceSnapshotId', 'type': 'str'},
    {'name': 'AutoSnapshotPolicyId', 'type': 'str'},
    {'name': 'EnableAutomatedSnapshotPolicy', 'type': 'str'},
    {'name': 'IOPSWrite', 'type': 'int'},
    {'name': 'InstanceId', 'type': 'str'},
    {'name': 'IOPS', 'type': 'int'},
    {'name': 'RegionId', 'type': 'str'},
    {'name': 'ExpiredTime', 'type': 'str'},
    {'name': 'Size', 'type': 'int'},
    {'name': 'ResourceGroupId', 'type': 'str'},
    {'name': 'DiskChargeType', 'type': 'str'},
    {'name': 'ZoneId', 'type': 'str'},
    {'name': 'AttachedTime', 'type': 'str'},
    {'name': 'Category', 'type': 'str'},
    {'name': 'ProductCode', 'type': 'str'},
    {'name': 'MultiAttach', 'type': 'str'},
    {'name': 'OperationLocks', 'type': 'dict'},
    {'name': 'MountInstances', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'Attachments', 'type': 'dict'},
    {'name': 'ProvisionedIops', 'type': 'int'},
    {'name': 'BurstingEnabled', 'type': 'str'},
    {'name': 'Throughput', 'type': 'int'}
]
nat_interface_columns = [
    {'name': 'id', 'type': 'str'},
    {'name': 'router_id', 'type': 'str'},
    {'name': 'status', 'type': 'str'},
    {'name': 'description', 'type': 'str'},
    {'name': 'admin_state_up', 'type': 'str'},
    {'name': 'tenant_id', 'type': 'str'},
    {'name': 'created_at', 'type': 'str'},
    {'name': 'spec', 'type': 'str'},
    {'name': 'internal_network_id', 'type': 'str'},
    {'name': 'name', 'type': 'str'},
    {'name': 'enterprise_project_id', 'type': 'str'}
]
sg_interface_columns = [
    {'name': 'SecurityGroupId', 'type': 'str'},
    {'name': 'SecurityGroupName', 'type': 'str'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'SecurityGroupType', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'CreationTime', 'type': 'str'},
    {'name': 'EcsCount', 'type': 'int'},
    {'name': 'AvailableInstanceAmount', 'type': 'int'},
    {'name': 'ResourceGroupId', 'type': 'str'},
    {'name': 'ServiceManaged', 'type': 'str'},
    {'name': 'ServiceID', 'type': 'str'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'Permissions', 'type': 'dict'}
]

ecs_field_document = 'https://help.aliyun.com/document_detail/25506.html?spm=a2c4g.11186623.0.0.3ac56cf0qyfOQ7#resultMapping'
eip_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeEipAddresses#workbench-doc-params'
nat_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeNatGateways#workbench-doc-response'
network_interface_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeNetworkInterfaces'
disk_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeDisks'
sg_field_document = 'https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeSecurityGroups'


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


@cloud_providers.aliyun.register('disk')
class Disk(Ecs):
    _des_request = DescribeDisksRequest
    _response_field = 'Disks'
    _child_response_filed = 'Disk'

    _table_name = 'aliyun_disk'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in disk_interface_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'disk_id', name='aliyun_uc_disk'),)
    _field_document = disk_field_document


@cloud_providers.aliyun.register('security_groups')
class Sg(Ecs):
    _des_request = DescribeSecurityGroupsRequest
    _response_field = 'SecurityGroups'
    _child_response_filed = 'SecurityGroup'

    _table_name = 'aliyun_sg'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in sg_interface_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'security_group_id', name='aliyun_uc_sg'),)
    _field_document = sg_field_document

    def _paginate_all_assets(self):
        assets = super(Sg, self)._paginate_all_assets()
        for asset in assets:
            sg_id = asset['SecurityGroupId']
            request = DescribeSecurityGroupAttributeRequest()
            request.set_query_params({'SecurityGroupId': sg_id, 'RegionId': self.region})
            response = self._describe(
                self.client,
                request,
                'Permissions',
                'Permission',
                self.parser_response
            ).parser_response()
            if not response:
                continue
            asset['Permissions'] = response

        return assets

