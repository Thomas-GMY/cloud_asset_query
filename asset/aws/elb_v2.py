# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import copy

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

elbv2_filed_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers'
elbv2_listener_filed_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_listeners'
elbv2_tgs_filed_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups'
elbv2_tgs_health_filed_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health'

elbv2_asset_columns = [
    {'name': 'LoadBalancerArn', 'type': 'str'},
    {'name': 'DNSName', 'type': 'str'},
    {'name': 'CanonicalHostedZoneId', 'type': 'str'},
    {'name': 'CreatedTime', 'type': 'date'},
    {'name': 'LoadBalancerName', 'type': 'str'},
    {'name': 'Scheme', 'type': 'str'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'State', 'type': 'dict'},
    {'name': 'Type', 'type': 'str'},
    {'name': 'AvailabilityZones', 'type': 'dict'},
    {'name': 'SecurityGroups', 'type': 'dict'},
    {'name': 'IpAddressType', 'type': 'str'},
    {'name': 'CustomerOwnedIpv4Pool', 'type': 'str'},
    {'name': 'Tags', 'type': 'list'},
]
elbv2_listener_asset_columns = [
    {'name': 'ListenerArn', 'type': 'str'},
    {'name': 'LoadBalancerArn', 'type': 'str'},
    {'name': 'Port', 'type': 'int'},
    {'name': 'Protocol', 'type': 'str'},
    {'name': 'Certificates', 'type': 'dict'},
    {'name': 'SslPolicy', 'type': 'str'},
    {'name': 'DefaultActions', 'type': 'dict'},
    {'name': 'AlpnPolicy', 'type': 'dict'}
]

elbv2_tgs_asset_columns = [
    {'name': 'TargetGroupArn', 'type': 'str'},
    {'name': 'TargetGroupName', 'type': 'str'},
    {'name': 'Protocol', 'type': 'str'},
    {'name': 'Port', 'type': 'int'},
    {'name': 'VpcId', 'type': 'str'},
    {'name': 'HealthCheckProtocol', 'type': 'str'},
    {'name': 'HealthCheckPort', 'type': 'str'},
    {'name': 'HealthCheckEnabled', 'type': 'str'},
    {'name': 'HealthCheckIntervalSeconds', 'type': 'int'},
    {'name': 'HealthCheckTimeoutSeconds', 'type': 'int'},
    {'name': 'HealthyThresholdCount', 'type': 'int'},
    {'name': 'UnhealthyThresholdCount', 'type': 'int'},
    {'name': 'HealthCheckPath', 'type': 'str'},
    {'name': 'Matcher', 'type': 'dict'},
    {'name': 'LoadBalancerArns', 'type': 'dict'},
    {'name': 'TargetType', 'type': 'str'},
    {'name': 'ProtocolVersion', 'type': 'str'},
    {'name': 'IpAddressType', 'type': 'str'}
]
elbv2_tas_health_asset_columns = [
    # {'name': 'Target', 'type': 'dict'},
    {'name': 'Id', 'type': 'str'},
    {'name': 'Port', 'type': 'int'},
    {'name': 'HealthCheckPort', 'type': 'str'},
    {'name': 'TargetHealth', 'type': 'dict'},
    {'name': 'TargetGroupArn', 'type': 'str'}
]


@cloud_providers.aws.register('elb_v2')
class ElbV2(AwsAsset):
    _client_name = 'elbv2'
    _des_request = 'describe_load_balancers'
    _response_field = 'LoadBalancers'
    _des_request_kwargs: dict = {'PageSize': 100}

    _table_name = 'aws_elb_v2'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in elbv2_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'load_balancer_arn', name='aws_uc_elbv2'),)
    _field_document = elbv2_filed_document

    def _paginate_all_assets(self) -> list:
        tags = []
        _des_request_kwargs = copy.deepcopy(self._des_request_kwargs)
        _assets, _ = self._describe(
            self.client,
            self._des_request,
            self._response_field,
            self._child_response_filed,
            des_request_kwargs=_des_request_kwargs,
            parser_response_func=self.parser_response
        ).parser_response()

        for index in range(len(_assets) // 20 + 1):
            """get tags"""
            elb_list = _assets[index: 20: index * 20 + 20]
            if elb_list:
                break
            _tags, _ = self._describe(
                self.client,
                'describe_tags',
                'TagDescriptions',
                des_request_kwargs={'ResourceArns': [elb['LoadBalancerArn'] for elb in elb_list]},
                parser_response_func=self.parser_response
            )
            tags += _tags
        for asset in _assets:
            try:
                tag = filter(lambda x: x['LoadBalancerArn'] == asset['LoadBalancerArn'], tags).__next__()
            except Exception as e:
                tag = []
            asset.update({'Tags': tag})
        return _assets


@cloud_providers.aws.register('elb_v2_listeners')
class ElbV2Listeners(AwsAsset):
    _client_name = 'elbv2'
    _des_request = 'describe_listeners'
    _response_field = 'Listeners'
    _des_request_kwargs: dict = {'PageSize': 50}
    _next_type = 'Marker'

    _table_name = 'aws_elb_v2_listener'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in elbv2_listener_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'listener_arn', name='aws_uc_elbv2_listener'),)
    _field_document = elbv2_listener_filed_document

    def _paginate_all_assets(self) -> list:
        assets = []
        elb_list = ElbV2(self.cred, self.region, dbconfig=self.dbconfig).paginate_all_assets
        _des_request_kwargs = copy.deepcopy(self._des_request_kwargs)

        for elb in elb_list:
            elb_arn = elb['LoadBalancerArn']
            while True:
                _des_request_kwargs.update({'LoadBalancerArn': elb_arn})
                _assets, next_token = self._describe(
                    self.client,
                    self._des_request,
                    self._response_field,
                    self._child_response_filed,
                    des_request_kwargs=_des_request_kwargs,
                    parser_response_func=self.parser_response
                ).parser_response()
                assets += _assets
                if next_token is None:
                    break
                _des_request_kwargs.update({self._next_type: next_token})
        return assets


@cloud_providers.aws.register('elb_v2_target_groups')
class ElbV2TargetGroups(AwsAsset):
    _client_name = 'elbv2'
    _des_request = 'describe_target_groups'
    _response_field = 'TargetGroups'
    _des_request_kwargs: dict = {'PageSize': 50}
    _next_type = 'Marker'

    _table_name = 'aws_elb_v2_target_groups'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in elbv2_tgs_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'target_group_arn', name='aws_uc_elbv2_target_groups'),)
    _field_document = elbv2_tgs_filed_document


@cloud_providers.aws.register('elb_v2_target_group_health')
class ElbV2TargetGroupHealth(AwsAsset):
    _client_name = 'elbv2'
    _des_request = 'describe_target_health'
    _response_field = 'TargetHealthDescriptions'
    _des_request_kwargs: dict = {'PageSize': 50}
    _next_type = 'Marker'

    _table_name = 'aws_elb_v2_target_group_health'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in elbv2_tas_health_asset_columns]
    _table_args = (
        UniqueConstraint('account_id', 'record_date', 'id', 'target_group_arn',  name='aws_uc_elbv2_tg_health'),)
    _field_document = elbv2_tgs_health_filed_document

    def _paginate_all_assets(self) -> list:
        assets = []
        target_groups = ElbV2TargetGroups(self.cred, region=self.region, dbconfig=self.dbconfig).paginate_all_assets
        for target_group in target_groups:
            arn = target_group['TargetGroupArn']
            _assets, _ = self._describe(
                self.client,
                self._des_request,
                self._response_field,
                self._child_response_filed,
                des_request_kwargs={'TargetGroupArn': arn},
                parser_response_func=self.parser_response
            ).parser_response()
            for _asset in _assets:
                _asset.update(_asset.pop('Target'))
                _asset.update({'TargetGroupArn': arn})
            assets += _assets
        return assets
