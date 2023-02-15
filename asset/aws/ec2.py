# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

ec2_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances'
nat_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_nat_gateways'
vpc_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs'
subnet_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets'
sg_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets'
nt_filed_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces'

ec2_asset_columns = [
    {'name': 'AmiLaunchIndex ', 'type': 'int'},
    {'name': 'ImageId', 'type': 'str', 'len': 64},
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'InstanceType', 'type': 'str', 'len': 16},
    {'name': 'KernelId', 'type': 'str', 'len': 64},
    {'name': 'KeyName', 'type': 'str', 'len': 32},
    {'name': 'LaunchTime', 'type': 'date'},
    {'name': 'Monitoring', 'type': 'dict'},
    {'name': 'Placement', 'type': 'dict'},
    {'name': 'PlatformDetails', 'type': 'str', 'len': 16},
    {'name': 'PrivateDnsName', 'type': 'str', 'len': 128},
    {'name': 'PrivateIpAddress', 'type': 'str', 'len': 32},
    {'name': 'ProductCodes', 'type': 'dict'},
    {'name': 'PublicDnsName', 'type': 'str', 'len': 128},
    {'name': 'PublicIpAddress', 'type': 'str', 'len': 128},
    {'name': 'RamdiskId', 'type': 'str', 'len': 128},
    {'name': 'State', 'type': 'dict'},
    {'name': 'StateTransitionReason', 'type': 'str', 'len': 128},
    {'name': 'SubnetId', 'type': 'str', 'len': 64},
    {'name': 'VpcId', 'type': 'str', 'len': 64},
    {'name': 'Architecture', 'type': 'str', 'len': 32},
    {'name': 'BlockDeviceMappings', 'type': 'dict'},
    {'name': 'ClientToken', 'type': 'str', 'len': 128},
    {'name': 'EbsOptimized', 'type': 'bool'},
    {'name': 'EnaSupport', 'type': 'bool'},
    {'name': 'Hypervisor', 'type': 'str', 'len': 8},
    {'name': 'IamInstanceProfile', 'type': 'dict'},
    {'name': 'InstanceLifecycle', 'type': 'str', 'len': 8},
    {'name': 'ElasticGpuAssociations', 'type': 'dict'},
    {'name': 'ElasticInferenceAcceleratorAssociations', 'type': 'dict'},
    {'name': 'NetworkInterfaces', 'type': 'dict'},
    {'name': 'OutpostArn', 'type': 'str', 'len': 64},
    {'name': 'RootDeviceName', 'type': 'str', 'len': 64},
    {'name': 'RootDeviceType', 'type': 'str', 'len': 16},
    {'name': 'SecurityGroups', 'type': 'dict'},
    {'name': 'SourceDestCheck', 'type': 'bool'},
    {'name': 'SpotInstanceRequestId', 'type': 'str', 'len': 64},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'VirtualizationType', 'type': 'str', 'len': 32},
    {'name': 'HibernationOptions', 'type': 'dict'},
    {'name': 'Licenses', 'type': 'dict'},
    {'name': 'Ipv6Address', 'type': 'str', 'len': 64},
]
nat_asset_columns = [
    {'name': 'CreateTime', 'type': 'datetime'},
    {'name': 'DeleteTime', 'type': 'datetime'},
    {'name': 'FailureCode', 'type': 'str'},
    {'name': 'FailureMessage', 'type': 'str'},
    {'name': 'NatGatewayAddresses', 'type': 'dict'},
    {'name': 'NatGatewayId', 'type': 'str'},
    {'name': 'ProvisionedBandwidth', 'type': 'dict'},
    {'name': 'State', 'type': 'str'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'ConnectivityType', 'type': 'str'}
]
vpc_asset_columns = [
    {'name': 'CidrBlock', 'type': 'str'},
    {'name': 'DhcpOptionsId', 'type': 'str'},
    {'name': 'State', 'type': 'str', 'length': 16},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'OwnerId', 'type': 'str'},
    {'name': 'InstanceTenancy', 'type': 'str', 'length': 16},
    {'name': 'Ipv6CidrBlockAssociationSet', 'type': 'dict'},
    {'name': 'CidrBlockAssociationSet', 'type': 'dict'},
    {'name': 'IsDefault', 'type': 'bool'},
    {'name': 'Tags', 'type': 'dict'}
]
subnet_asset_columns = [
    {'name': 'AvailabilityZone', 'type': 'str'},
    {'name': 'AvailabilityZoneId', 'type': 'str'},
    {'name': 'AvailableIpAddressCount', 'type': 'int'},
    {'name': 'CidrBlock', 'type': 'str'},
    {'name': 'DefaultForAz', 'type': 'bool'},
    {'name': 'EnableLniAtDeviceIndex', 'type': 'int'},
    {'name': 'MapPublicIpOnLaunch', 'type': 'bool'},
    {'name': 'MapCustomerOwnedIpOnLaunch', 'type': 'bool'},
    {'name': 'CustomerOwnedIpv4Pool', 'type': 'str'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'OwnerId', 'type': 'str'},
    {'name': 'AssignIpv6AddressOnCreation', 'type': 'bool'},
    {'name': 'Ipv6CidrBlockAssociationSet', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'SubnetArn', 'type': 'str'},
    {'name': 'OutpostArn', 'type': 'str'},
    {'name': 'EnableDns64', 'type': 'bool'},
    {'name': 'Ipv6Native', 'type': 'bool'},
    {'name': 'PrivateDnsNameOptionsOnLaunch', 'type': 'dict'}
]
sg_asset_columns = [
    {'name': 'Description', 'type': 'str'},
    {'name': 'GroupName', 'type': 'str'},
    {'name': 'IpPermissions', 'type': 'dict'},
    {'name': 'OwnerId', 'type': 'str'},
    {'name': 'GroupId', 'type': 'str'},
    {'name': 'IpPermissionsEgress', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'VpcId', 'type': 'str'}
]
nt_asset_columns = [
    {'name': 'Association', 'type': 'dict'},
    {'name': 'Attachment', 'type': 'dict'},
    {'name': 'AvailabilityZone', 'type': 'str'},
    {'name': 'Description', 'type': 'text'},
    {'name': 'Groups', 'type': 'dict'},
    {'name': 'InterfaceType', 'type': 'str'},
    {'name': 'Ipv6Addresses', 'type': 'dict'},
    {'name': 'MacAddress', 'type': 'str'},
    {'name': 'NetworkInterfaceId', 'type': 'str'},
    {'name': 'OutpostArn', 'type': 'str'},
    {'name': 'OwnerId', 'type': 'str'},
    {'name': 'PrivateDnsName', 'type': 'str'},
    {'name': 'PrivateIpAddress', 'type': 'str'},
    {'name': 'PrivateIpAddresses', 'type': 'dict'},
    {'name': 'Ipv4Prefixes', 'type': 'dict'},
    {'name': 'Ipv6Prefixes', 'type': 'dict'},
    {'name': 'RequesterId', 'type': 'str'},
    {'name': 'RequesterManaged', 'type': 'bool'},
    {'name': 'SourceDestCheck', 'type': 'bool'},
    {'name': 'Status', 'type': 'str', 'length': 16},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'DenyAllIgwTraffic', 'type': 'bool'},
    {'name': 'Ipv6Native', 'type': 'bool'},
    {'name': 'Ipv6Address', 'type': 'str'}
]


@cloud_providers.aws.register('ec2')
class Ec2(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_instances'
    _response_field = 'Reservations'
    _child_response_filed = 'Instances'

    _table_name = 'aws_ec2'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ec2_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='aws_uc_ec2'),)
    _field_document = ec2_field_document


@cloud_providers.aws.register('nat_gateways')
class NatGateways(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_nat_gateways'
    _response_field = 'NatGateways'

    _table_name = 'aws_nat_gateways'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in nat_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'nat_gateway_id', name='aws_uc_nat_g'),)
    _field_document = nat_field_document


@cloud_providers.aws.register('vpc')
class Vpc(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_vpcs'
    _response_field = 'Vpcs'

    _table_name = 'aws_vpcs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in vpc_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'vpc_id', name='aws_uc_vpc'),)
    _field_document = vpc_field_document


@cloud_providers.aws.register('subnets')
class Subnets(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_subnets'
    _response_field = 'Subnets'

    _table_name = 'aws_subnets'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in subnet_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'subnet_id', name='aws_uc_subnets'),)
    _field_document = subnet_field_document


@cloud_providers.aws.register('security_groups')
class SecurityGroups(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_security_groups'
    _response_field = 'SecurityGroups'

    _table_name = 'aws_security_groups'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in sg_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'group_id', name='aws_uc_sg'),)
    _field_document = sg_field_document


@cloud_providers.aws.register('network_interfaces')
class NetworkInterfaces(AwsAsset):
    _client_name = 'ec2'
    _des_request = 'describe_network_interfaces'
    _response_field = 'NetworkInterfaces'

    _table_name = 'aws_network_interfaces'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in nt_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'network_interface_id', name='aws_uc_nt'),)
    _field_document = nt_filed_document



