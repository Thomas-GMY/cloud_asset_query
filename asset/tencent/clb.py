# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from tencentcloud.clb.v20180317.clb_client import ClbClient, models

asset_columns = [
    {'name': 'LoadBalancerId', 'type': 'str'},
    {'name': 'LoadBalancerName', 'type': 'str'},
    {'name': 'Forward', 'type': 'int'},
    {'name': 'Domain', 'type': 'str'},
    {'name': 'LoadBalancerVips', 'type': 'dict'},
    {'name': 'LoadBalancerType', 'type': 'str'},
    {'name': 'Status', 'type': 'int'},
    {'name': 'CreateTime', 'type': 'str'},
    {'name': 'StatusTime', 'type': 'str'},
    {'name': 'ProjectId', 'type': 'int'},
    {'name': 'OpenBgp', 'type': 'int'},
    {'name': 'Snat', 'type': 'str'},
    {'name': 'Isolation', 'type': 'int'},
    {'name': 'Log', 'type': 'str'},
    {'name': 'AnycastZone', 'type': 'str'},
    {'name': 'AddressIPVersion', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'NumericalVpcId', 'type': 'int'},
    # {'name': 'TargetRegionInfo', 'type': 'dict'},
    {'name': 'SubnetId', 'type': 'str'},
    {'name': 'SecureGroups', 'type': 'dict'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'VipIsp', 'type': 'str'},
    {'name': 'MasterZone', 'type': 'dict'},
    {'name': 'BackupZoneSet', 'type': 'dict'},
    {'name': 'IsolatedTime', 'type': 'str'},
    {'name': 'ExpireTime', 'type': 'str'},
    {'name': 'ChargeType', 'type': 'str'},
    {'name': 'NetworkAttributes', 'type': 'dict'},
    {'name': 'PrepaidAttributes', 'type': 'dict'}
]

clb_field_document = 'https://cloud.tencent.com/document/api/214/30685'


@cloud_providers.tencent.register('clb')
class Clb(TencentAsset):
    _des_request_func = 'DescribeLoadBalancers'
    _des_request = models.DescribeLoadBalancersRequest()
    _response_field = 'LoadBalancerSet'

    _table_name = 'tencent_clb'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'load_balancer_id', name='tencent_uc_clb'),)
    _field_document = clb_field_document

    def _get_client(self):
        return ClbClient(self.cred, self.region)
