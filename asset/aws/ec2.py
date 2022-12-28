# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import aws_asset_register
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances'
asset_columns = [
    {'name': 'AmiLaunchIndex ', 'type': 'int'},
    {'name': 'ImageId', 'type': 'str', 'len': 64},
    {'name': 'InstanceId', 'type': 'str', 'len': 64},
    {'name': 'InstanceType', 'type': 'str', 'len': 16},
    {'name': 'KernelId', 'type': 'str', 'len': 64},
    {'name': 'KeyName', 'type': 'str', 'len': 32},
    {'name': 'LaunchTime', 'type': 'date'},
    {'name': 'Monitoring', 'type': 'dict'},
    {'name': 'Placement', 'type': 'dict'},
    {'name': 'Platform', 'type': 'str', 'len': 16},
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


@aws_asset_register.register('ec2')
class Ec2(AwsAsset):
    _asset_name = 'ec2'
    _des_request = 'describe_instances'
    _response_field = 'Instances'

    _table_name = 'aws_ec2'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'instance_id', name='aws_instance'),)
    _field_document = field_document
