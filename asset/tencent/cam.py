# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0


from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from tencentcloud.cam.v20190116.cam_client import CamClient, models


user_asset_columns = [
    {'name': 'Uin', 'type': 'str'},
    {'name': 'Name', 'type': 'str'},
    {'name': 'Uid', 'type': 'str'},
    {'name': 'Remark', 'type': 'str'},
    {'name': 'ConsoleLogin', 'type': 'str'},
    {'name': 'PhoneNum', 'type': 'str'},
    {'name': 'CountryCode', 'type': 'str'},
    {'name': 'Email', 'type': 'str'},
    {'name': 'CreateTime', 'type': 'str'}
]
user_ak_asset_columns = [
    {'name': 'AccessKeyId', 'type': 'str'},
    {'name': 'Status', 'type': 'str'},
    {'name': 'CreateTime', 'type': 'str'},
    {'name': 'LastUse', 'type': 'dict'},
]
role_columns = [
    {'name': 'AddTime', 'type': 'str'},
    {'name': 'ConsoleLogin', 'type': 'int'},
    {'name': 'DeletionTaskId', 'type': 'str'},
    {'name': 'Description', 'type': 'str'},
    {'name': 'PolicyDocument', 'type': 'str'},
    {'name': 'RoleId', 'type': 'str'},
    {'name': 'RoleName', 'type': 'str'},
    {'name': 'RoleType', 'type': 'str'},
    {'name': 'SessionDuration', 'type': 'int'},
    {'name': 'Tags', 'type': 'dict'},
    {'name': 'UpdateTime', 'type': 'str'}
]
user_asset_document = 'https://cloud.tencent.com/document/api/598/34587'
user_ak_asset_document = 'https://cloud.tencent.com/document/api/598/45156'
role_asset_document = 'https://cloud.tencent.com/document/api/598/36223'



@cloud_providers.tencent.register('user')
class User(TencentAsset):
    _des_request_func = 'ListUsers'
    _des_request = models.ListUsersRequest()
    _response_field = 'Data'

    _paginate = False

    _table_name = 'tencent_user'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in user_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'uid', name='tencent_uc_user'),)
    _field_document = user_asset_document

    def _get_client(self):
        return CamClient(self.cred, self.region)


@cloud_providers.tencent.register('user_ak')
class UserAk(User):
    _des_request_func = 'ListAccessKeys'
    _des_request = models.ListAccessKeysRequest()
    _response_field = 'AccessKeys'

    _paginate = False

    _table_name = 'tencent_user_ak'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in user_ak_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'access_key_id', name='tencent_uc_user_ak'),)
    _field_document = user_ak_asset_document

    def _paginate_all_assets(self):
        assets = []
        users = User(self.cred, region=self.region, dbconfig=self.dbconfig)._paginate_all_assets()
        for user in users:
            self._des_request.TargetUin = user['Uin']
            response = self._describe(
                self.client, self._des_request_func, self._des_request, self._response_field).parser_response()
            if not response:
                break

            assets += response
        if not assets:
            return assets

        # get ak details
        request = models.GetSecurityLastUsedRequest()
        request.SecretIdList = [asset['AccessKeyId'] for asset in assets]
        response = self._describe(
            self.client,
            'GetSecurityLastUsed',
            request,
            'SecretIdLastUsedRows'
        ).parser_response()
        for asset in assets:
            asset['LastUse'] = list(filter(lambda x: x['SecretId'] == asset['AccessKeyId'], response))

        return assets


# @cloud_providers.tencent.register('role')
# class Role(TencentAsset):
#     pass


