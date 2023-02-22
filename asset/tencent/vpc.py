# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import copy

from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from tencentcloud.vpc.v20170312.vpc_client import VpcClient, models

vpc_asset_columns = [
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'VpcName', 'type': 'str'},
    {'name': 'CidrBlock', 'type': 'str'},
    {'name': 'Ipv6CidrBlock', 'type': 'str'},
    {'name': 'IsDefault', 'type': 'str'},
    {'name': 'EnableMulticast', 'type': 'str'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'EnableDhcp', 'type': 'str'},
    {'name': 'DhcpOptionsId', 'type': 'str'},
    {'name': 'DnsServerSet', 'type': 'dict'},
    {'name': 'DomainName', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'},
    {'name': 'AssistantCidrSet', 'type': 'dict'}
]
subnet_asset_columns = [
    {'name': 'NetworkAclId', 'type': 'str'},
    {'name': 'RouteTableId', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'EnableBroadcast', 'type': 'str'},
    {'name': 'Zone', 'type': 'str'},
    {'name': 'Ipv6CidrBlock', 'type': 'str'},
    {'name': 'AvailableIpAddressCount', 'type': 'int'},
    {'name': 'IsRemoteVpcSnat', 'type': 'str'},
    {'name': 'SubnetName', 'type': 'str'},
    {'name': 'TotalIpAddressCount', 'type': 'int'},
    {'name': 'IsCdcSubnet', 'type': 'int'},
    {'name': 'CdcId', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'CidrBlock', 'type': 'str'},
    {'name': 'IsDefault', 'type': 'str'}
]
route_table_asset_columns = [
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'RouteTableId', 'type': 'str'},
    {'name': 'RouteTableName', 'type': 'str'},
    {'name': 'AssociationSet', 'type': 'dict'},
    {'name': 'RouteSet', 'type': 'dict'},
    {'name': 'Main', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'},
    {'name': 'LocalCidrForCcn', 'type': 'dict'},
    {'name': 'CreatedTime', 'type': 'str'}
]
eip_asset_columns = [
    {'name': 'AddressId', 'type': 'str'},
    {'name': 'AddressName', 'type': 'str'},
    {'name': 'AddressIp', 'type': 'str'},
    {'name': 'AddressStatus', 'type': 'str'},
    {'name': 'AddressType', 'type': 'str'},
    {'name': 'InstanceId', 'type': 'str'},
    {'name': 'NetworkInterfaceId', 'type': 'str'},
    {'name': 'PrivateAddressIp', 'type': 'str'},
    {'name': 'IsArrears', 'type': 'str'},
    {'name': 'IsBlocked', 'type': 'str'},
    {'name': 'IsEipDirectConnection', 'type': 'str'},
    {'name': 'EipAlgType', 'type': 'dict'},
    {'name': 'LocalBgp', 'type': 'str'},
    {'name': 'CascadeRelease', 'type': 'str'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'InternetChargeType', 'type': 'str'},
    {'name': 'Bandwidth', 'type': 'int'},
    {'name': 'InternetServiceProvider', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'}
]
network_interface_asset_columns = [
    {'name': 'MacAddress', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'Business', 'type': 'str'},
    {'name': 'Zone', 'type': 'str'},
    {'name': 'NetworkInterfaceId', 'type': 'str'},
    {'name': 'Primary', 'type': 'str'},
    {'name': 'CdcId', 'type': 'str'},
    {'name': 'PrivateIpAddressSet', 'type': 'dict'},
    {'name': 'NetworkInterfaceDescription', 'type': 'str'},
    {'name': 'Ipv6AddressSet', 'type': 'dict'},
    {'name': 'State', 'type': 'str'},
    {'name': 'GroupSet', 'type': 'dict'},
    {'name': 'Attachment', 'type': 'dict'},
    {'name': 'TagSet', 'type': 'dict'},
    {'name': 'EniType', 'type': 'int'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'NetworkInterfaceName', 'type': 'str'},
    {'name': 'AttachType', 'type': 'int'}
]
nat_asset_columns = [
    {'name': 'NatGatewayId', 'type': 'str'},
    {'name': 'NatGatewayName', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'State', 'type': 'str'},
    {'name': 'NetworkState', 'type': 'str'},
    {'name': 'InternetMaxBandwidthOut', 'type': 'int'},
    {'name': 'MaxConcurrentConnection', 'type': 'int'},
    {'name': 'SecurityGroupSet', 'type': 'dict'},
    {'name': 'ExclusiveGatewayBandwidth', 'type': 'int'},
    {'name': 'IsExclusive', 'type': 'str'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'DirectConnectGatewayIds', 'type': 'dict'},
    {'name': 'SourceIpTranslationNatRuleSet', 'type': 'dict'},
    {'name': 'PublicIpAddressSet', 'type': 'dict'},
    {'name': 'DestinationIpPortTranslationNatRuleSet', 'type': 'dict'},
    {'name': 'Zone', 'type': 'str'},
    {'name': 'TagSet', 'type': 'dict'}
]
security_group_asset_columns = [
    {'name': 'SecurityGroupId', 'type': 'str'},
    {'name': 'SecurityGroupName', 'type': 'str'},
    {'name': 'SecurityGroupDesc', 'type': 'str'},
    {'name': 'ProjectId', 'type': 'str'},
    {'name': 'IsDefault', 'type': 'str'},
    {'name': 'CreatedTime', 'type': 'str'},
    {'name': 'Ingress', 'type': 'dict'},
    {'name': 'Egress', 'type': 'dict'}
]

vpc_field_document = 'https://cloud.tencent.com/document/api/215/15778'
subnet_field_document = 'https://cloud.tencent.com/document/api/215/15784'
route_table_field_document = 'https://cloud.tencent.com/document/api/215/15763'
eip_field_document = 'https://cloud.tencent.com/document/api/215/16702'
network_interface_field_document = 'https://cloud.tencent.com/document/api/215/15817'
nat_field_document = 'https://cloud.tencent.com/document/api/215/36034'
security_group_field_document = 'https://cloud.tencent.com/document/api/215/15808'


@cloud_providers.tencent.register('vpcs')
class Vpc(TencentAsset):
    _des_request_func = 'DescribeVpcs'
    _des_request = models.DescribeVpcsRequest()
    _response_field = 'VpcSet'

    _paginate_type = 'str'

    _table_name = 'tencent_vpcs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in vpc_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'vpc_id', name='tencent_uc_vpc'),)
    _field_document = vpc_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('subnets')
class Subnet(TencentAsset):
    _des_request_func = 'DescribeSubnets'
    _des_request = models.DescribeSubnetsRequest()
    _response_field = 'SubnetSet'

    _paginate_type = 'str'

    _table_name = 'tencent_subnets'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in subnet_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'subnet_id', name='tencent_uc_subnet'),)
    _field_document = subnet_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('route_tables')
class RouteTable(TencentAsset):
    _des_request_func = 'DescribeRouteTables'
    _des_request = models.DescribeRouteTablesRequest()
    _response_field = 'RouteTableSet'

    _paginate_type = 'str'

    _table_name = 'tencent_route_tables'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in route_table_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'route_table_id', name='tencent_uc_rt'),)
    _field_document = route_table_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('eips')
class Eip(TencentAsset):
    _des_request_func = 'DescribeAddresses'
    _des_request = models.DescribeAddressesRequest()
    _response_field = 'AddressSet'

    _table_name = 'tencent_eips'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in eip_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'address_id', name='tencent_uc_eip'),)
    _field_document = eip_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('network_interfaces')
class NetworkInterfaces(TencentAsset):
    _des_request_func = 'DescribeNetworkInterfaces'
    _des_request = models.DescribeNetworkInterfacesRequest()
    _response_field = 'NetworkInterfaceSet'

    _table_name = 'tencent_network_interfaces'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in network_interface_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'network_interface_id', name='tencent_uc_nt'),)
    _field_document = network_interface_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('nats')
class Nat(TencentAsset):
    _des_request_func = 'DescribeNatGateways'
    _des_request = models.DescribeNetworkInterfacesRequest()
    _response_field = 'NatGatewaySet'

    _table_name = 'tencent_nats'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in nat_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'nat_gateway_id', name='tencent_uc_nat'),)
    _field_document = nat_field_document

    def _get_client(self):
        return VpcClient(self.cred, self.region)


@cloud_providers.tencent.register('security_groups')
class SecurityGroups(TencentAsset):
    _des_request_func = 'DescribeSecurityGroups'
    _des_request = models.DescribeSecurityGroupsRequest()
    _response_field = 'SecurityGroupSet'

    _paginate_type = 'str'

    _table_name = 'tencent_security_groups'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in security_group_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'security_group_id', name='tencent_uc_sg'),)
    _field_document = security_group_field_document

    def _paginate_all_assets(self):
        page, assets = 0, []
        _des_request = copy.deepcopy(self._des_request)
        _des_request.Limit = 50 if self._paginate_type == 'int' else '50'

        while True:
            response = self._describe(
                self.client, self._des_request_func, _des_request, self._response_field).parser_response()
            if not response:
                break
            for security_group in response:
                """get security group rules"""
                security_id = security_group['SecurityGroupId']
                rule_des_request = models.DescribeSecurityGroupPoliciesRequest()
                rule_des_request.SecurityGroupId = security_id

                rule = self._describe(
                    self.client,
                    'DescribeSecurityGroupPolicies',
                    rule_des_request,
                    'SecurityGroupPolicySet'
                ).parser_response()
                security_group['Ingress'] = rule.get('Ingress', [])
                security_group['Egress'] = rule.get('Egress', [])

            assets += response
            page = 1
            if isinstance(_des_request.Limit, str):
                _des_request.Offset = str(page * int(_des_request.Limit))
            else:
                _des_request.Offset = page * _des_request.Limit
        return assets

    def _get_client(self):
        return VpcClient(self.cred, self.region)

