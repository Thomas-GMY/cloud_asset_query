# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AliyunAsset, AssetColumn, UniqueConstraint
from aliyunsdkram.request.v20150501.ListUsersRequest import ListUsersRequest
from aliyunsdkram.request.v20150501.GetUserRequest import GetUserRequest
from aliyunsdkram.request.v20150501.GetLoginProfileRequest import GetLoginProfileRequest
from aliyunsdkram.request.v20150501.ListAccessKeysRequest import ListAccessKeysRequest


ram_asset_columns = [
    {'name': 'DisplayName', 'type': 'str'},
    {'name': 'Email', 'type': 'str'},
    {'name': 'UpdateDate', 'type': 'str'},
    {'name': 'MobilePhone', 'type': 'str'},
    {'name': 'UserId', 'type': 'str'},
    {'name': 'Comments', 'type': 'str'},
    {'name': 'CreateDate', 'type': 'str'},
    {'name': 'UserName', 'type': 'str'},
    {'name': 'LastLoginDate', 'type': 'dict'},
    {'name': 'LoginProfile', 'type': 'dict'},
    {'name': 'AccessKeys', 'type': 'list'},
]

ram_field_document = 'https://next.api.alibabacloud.com/document/Ram/2015-05-01/ListUsers'


@cloud_providers.aliyun.register('user')
class User(AliyunAsset):
    _des_request = ListUsersRequest
    _response_field = 'Users'
    _child_response_filed = 'User'

    _paginate = False

    _table_name = 'aliyun_user'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ram_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'user_id', name='aliyun_uc_user'),)
    _field_document = ram_field_document

    def _paginate_all_assets(self):
        assets = super()._paginate_all_assets()
        if not assets:
            return assets

        for asset in assets:
            request = GetUserRequest()
            request.set_UserName(asset['UserName'])
            last_login = self._describe(self.client, request, 'User').parser_response()
            if last_login:
                asset.update({'LastLoginDate': last_login['LastLoginDate']})

            # get loging profile
            last_login_request = GetLoginProfileRequest()
            last_login_request.set_UserName(asset['UserName'])
            login_profile = self._describe(self.client, last_login_request, 'LoginProfile').parser_response()

            if login_profile:
                asset.update({'LoginProfile': login_profile})

            # get access keys
            access_keys_request = ListAccessKeysRequest()
            access_keys_request.set_UserName(asset['UserName'])
            access_keys = self._describe(self.client, access_keys_request, 'AccessKeys').parser_response()
            if access_keys:
                asset.update({'AccessKeys': access_keys})

        return assets
