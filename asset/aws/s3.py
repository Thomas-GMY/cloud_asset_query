# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint


buckets_filed_document = """
    1、https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
    2、https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_acl
    3、https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy
    4、https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy_status
"""

buckets_asset_columns = [
    {'name': 'Name', 'type': 'str'},
    {'name': 'CreationDate', 'type': 'datetime'},
    {'name': 'BucketAclGrants', 'type': 'dict'},
    {'name': 'BucketPolicy', 'type': 'text'},
    {'name': 'BucketPolicyStatus', 'type': 'dict'},
]


@cloud_providers.aws.register('s3_buckets')
class S3Buckets(AwsAsset):
    _client_name = 's3'

    _table_name = 'aws_s3_buckets'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in buckets_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'name', name='aws_uc_s3b'),)
    _field_document = buckets_filed_document

    def _paginate_all_assets(self) -> list:
        assets = []
        buckets, _ = self._describe(
            self.client, 'list_buckets', 'Buckets', parser_response_func=self.parser_response).parser_response()
        for bucket in buckets:
            """get_bucket_acl"""
            des_request_kwargs = {'Bucket': bucket['Name']}
            try:
                bucket_acl_grants, _ = self._describe(
                    self.client, 'get_bucket_acl', 'Grants',
                    des_request_kwargs=des_request_kwargs, parser_response_func=self.parser_response
                ).parser_response()
            except Exception as error:
                bucket_acl_grants = [str(error)]

            try:
                bucket_policy, _ = self._describe(
                    self.client, 'get_bucket_policy', 'Policy',
                    des_request_kwargs=des_request_kwargs, parser_response_func=self.parser_response
                ).parser_response()
            except Exception as error:
                bucket_policy = str(error)

            try:
                bucket_policy_status, _ = self._describe(
                    self.client, 'get_bucket_policy_status', 'PolicyStatus',
                    des_request_kwargs=des_request_kwargs, parser_response_func=self.parser_response
                ).parser_response()
            except Exception as error:
                bucket_policy_status = {'error': str(error)}

            bucket.update(
                {
                    'BucketAclGrants': bucket_acl_grants,
                    'BucketPolicy': bucket_policy,
                    'BucketPolicyStatus': bucket_policy_status
                }
            )
            assets.append(bucket)
        return assets

