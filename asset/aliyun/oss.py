from asset.asset_register import cloud_providers
from asset.base import Asset, AssetColumn, UniqueConstraint
from asset.schema import DbConfig, RamRoleArnCredential
from asset.utils import aliyun_parser_response, get_aliyun_account_id
from typing import List 
from asset.schema import AliyunProfile

import oss2
from alibabacloud_credentials.client import Client
from alibabacloud_credentials.models import Config
from oss2 import CredentialsProvider
from oss2.credentials import Credentials
import datetime


asset_columns = [
    {'name': 'name', 'type': 'str', 'len': 64},
    {'name': 'extranet_endpoint', 'type': 'str', 'len': 128},
    {'name': 'intranet_endpoint', 'type': 'str', 'len': 64},
    {'name': 'location', 'type': 'str', 'len': 64},
    {'name': 'resource_group_id', 'type': 'str', 'len': 64},
    {'name': 'storage_class', 'type': 'str', 'len': 64},
    {'name': 'acl', 'type': 'str', 'len': 64},
    {'name': 'creation_date', 'type': 'datetime'},
]


class CredentialProviderWarpper(CredentialsProvider):
    def __init__(self, client):
        self.client = client

    def get_credentials(self):
        access_key_id = self.client.get_access_key_id()
        access_key_secret = self.client.get_access_key_secret()
        security_token = self.client.get_security_token()
        return Credentials(access_key_id, access_key_secret, security_token)


def timestamp_to_date(timestamp: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


@cloud_providers.aliyun.register('oss')
class Oss(Asset):
    _platform = 'aliyun'

    _table_name = 'oss'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'name', name='aliyun_oss_'),)

    def _paginate_all_assets(self) -> list:
        assets = []
        auth, endpoint = self._get_client()
        bucket_endpoint = 'https://{location}.aliyuncs.com'

        # get buckets
        print(self.region, endpoint, 22222222222)
        for b in oss2.BucketIterator(oss2.Service(auth, endpoint)):
            b_dict = b.__dict__
            b_dict['creation_date'] = timestamp_to_date(b_dict['creation_date'])
            # get acl
            b_dict['acl'] = oss2.Bucket(auth, endpoint=bucket_endpoint.format(location=b.location), bucket_name=b.name).get_bucket_acl().acl
            assets.append(b_dict)

        return assets

    def _get_assets(self) -> list:
        pass

    def _get_client(self) -> (oss2.ProviderAuth, str):
        config = Config(
            type='ram_role_arn',
            # 从环境变量中获取RAM用户的访问密钥（AccessKey ID和AccessKey Secret）。                  
            access_key_id=self.cred.sts_access_key_id,          
            access_key_secret=self.cred.sts_access_key_secret,  
            # 从环境变量中获取RAM角色的RamRoleArn。
            role_arn=self.cred.role_arn,
            # 填写RAM角色的会话名称。
            role_session_name=self.cred.session_role_name
        )

        cred = Client(config)

        credentials_provider = CredentialProviderWarpper(cred)

        # 使用环境变量中获取的RAM用户的访问密钥和RAM角色的RamRoleArn配置访问凭证。
        auth = oss2.ProviderAuth(credentials_provider)
        endpoint = f'https://oss-{self.region}.aliyuncs.com'
        return auth, endpoint


    def _get_account_id(self):
        return get_aliyun_account_id(cred=self.cred)

    @classmethod
    def load_creds(cls, profile: AliyunProfile) -> List[RamRoleArnCredential]:
        return [
            RamRoleArnCredential(
                profile.ak,
                profile.sk,
                role.arn,
                role.session_name
            ) for role in profile.roles
        ]




