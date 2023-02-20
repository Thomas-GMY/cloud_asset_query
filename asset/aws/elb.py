# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import copy

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers'


asset_columns = [
    {'name': 'LoadBalancerName', 'type': 'str'},
    {'name': 'DNSName', 'type': 'str'},
    {'name': 'CanonicalHostedZoneName', 'type': 'str'},
    {'name': 'CanonicalHostedZoneNameID', 'type': 'str'},
    {'name': 'ListenerDescriptions', 'type': 'dict'},
    {'name': 'Policies', 'type': 'dict'},
    {'name': 'BackendServerDescriptions', 'type': 'dict'},
    {'name': 'AvailabilityZones', 'type': 'dict'},
    {'name': 'Subnets', 'type': 'dict'},
    {'name': 'VPCId', 'type': 'str'},
    {'name': 'Instances', 'type': 'dict'},
    {'name': 'HealthCheck', 'type': 'dict'},
    {'name': 'SourceSecurityGroup', 'type': 'dict'},
    {'name': 'SecurityGroups', 'type': 'dict'},
    {'name': 'CreatedTime', 'type': 'date'},
    {'name': 'Scheme', 'type': 'str'},
    {'name': 'Tags', 'type': 'dict'}
]


@cloud_providers.aws.register('elb')
class Elb(AwsAsset):
    _client_name = 'elb'
    _des_request = 'describe_load_balancers'
    _response_field = 'LoadBalancerDescriptions'
    _des_request_kwargs: dict = {'PageSize': 400}

    _table_name = 'aws_elb'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'load_balancer_name', name='aws_uc_elb'),)
    _field_document = field_document

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
                des_request_kwargs={'LoadBalancerNames': [elb['LoadBalancerNames']for elb in elb_list]},
                parser_response_func=self.parser_response
            )
            tags += _tags
        if tags:
            for asset in _assets:
                try:
                    tag = filter(lambda x: x['LoadBalancerName'] == asset['LoadBalancerName'], tags).__next__()
                except Exception as e:
                    tag = []
                asset.update({'Tags': tag})
        return _assets




