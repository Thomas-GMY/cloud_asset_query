# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import HuaweiAsset, AssetColumn, UniqueConstraint

from huaweicloudsdkvpc.v3.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v3.vpc_client import VpcClient
from huaweicloudsdkvpc.v3.model import ListSecurityGroupsRequest, ListSecurityGroupRulesRequest


sg_asset_columns = [
    {'name': 'id', 'type': 'str'},
    {'name': 'name', 'type': 'str'},
    {'name': 'description', 'type': 'str'},
    {'name': 'vpc_id', 'type': 'str'},
    {'name': 'enterprise_project_id', 'type': 'str'},
    {'name': 'security_group_rules', 'type': 'dict'}
]

sg_field_document = 'https://support.huaweicloud.com/api-vpc/vpc_sg01_0003.html'


@cloud_providers.huawei.register('security_groups')
class SecurityGroup(HuaweiAsset):
    _client = VpcClient
    _region_obj = VpcRegion
    _des = 'list_security_groups'
    _request_obj = ListSecurityGroupsRequest
    _response_field = 'security_groups'
    _request_pars = {}
    _offset = False

    _table_name = 'huawei_sg'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in sg_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'id', name='huawei_uc_sg'),)
    _field_document = sg_field_document

    def _paginate_all_assets(self) -> list:
        assets = super(SecurityGroup, self)._paginate_all_assets()
        if not assets:
            return assets

        # find sg detail
        sg_ids = [asset['id'] for asset in assets]
        request = ListSecurityGroupRulesRequest(security_group_id=sg_ids)
        responses = self._describe(
            self.client,
            'list_security_group_rules',
            request,
            'security_group_rules',
            self.parser_response
        ).parser_response()
        for asset in assets:
            asset['security_group_rules'] = list(filter(lambda x: x['security_group_id'] == asset['id'], responses))

        return assets
