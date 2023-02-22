# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import TencentAsset, AssetColumn, UniqueConstraint
from qcloud_cos import CosConfig, CosS3Client

cos_asset_columns = [
    {'name': 'Name', 'type': 'str'},
    {'name': 'Location', 'type': 'str'},
    {'name': 'CreationDate', 'type': 'str'},
    {'name': 'OwnerDisplayName', 'type': 'str'},
    {'name': 'OwnerId', 'type': 'str'},
]

cos_field_document = 'https://cloud.tencent.com/document/product/436/35150'


@cloud_providers.tencent.register('cos')
class Cos(TencentAsset):
    _des_request_func = 'list_buckets'
    _response_field = 'Buckets'

    _table_name = 'tencent_cos'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in cos_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'name', name='tencent_uc_cos'),)
    _field_document = cos_field_document

    def _paginate_all_assets(self):
        assets = []
        config = CosConfig(
            Region=self.region, SecretId=self.cred.secretId, SecretKey=self.cred.secretKey, Token=self.cred.token)
        client = CosS3Client(config)
        response = client.list_buckets()

        owner = response.get('Owner', {})
        bucket_dict = response.get('Buckets', {})

        if not bucket_dict:
            return assets

        for asset in bucket_dict.get('Bucket', []):
            asset.update(
                {
                    'OwnerDisplayName': owner.get('DisplayName', ''),
                    'OwnerId': owner.get('ID', '')
                }
            )
            assets.append(asset)
        return assets

    def _get_client(self):
        pass
