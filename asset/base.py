# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import abc
import copy
import datetime

from typing import List

from sqlalchemy import create_engine, Table, UniqueConstraint

from boto3 import Session

from asset.asset_table import AssetTable
from asset.schema import DbConfig, AssetColumn, STSAssumeRoleCredential, RamRoleArnCredential, AwsCredential,\
    TencentProfile, AliyunProfile, AwsProfile
from asset.utils import to_hump_underline, get_tencent_account_id, get_aliyun_account_id, get_aws_account_id, \
    tencent_parser_response, aliyun_parser_response, aws_parser_response, recursive_list, aws_assume_role


class Describe:
    def parser_response(self):
        raise NotImplementedError("")

    def describe(self):
        raise NotImplementedError("")


class DescribeTencent(Describe):

    def __init__(
            self,
            client,
            des_request_func: str,
            des_request,
            response_filed: str,
            parser_response: callable = tencent_parser_response
    ):
        self.client = client
        self.des_request_func = des_request_func
        self.des_request = des_request
        self.response_field = response_filed
        self.parser_response_func = parser_response

    def parser_response(self):
        return self.parser_response_func(self.describe(), self.response_field)

    def describe(self):
        return getattr(self.client, self.des_request_func)(self.des_request)


class DescribeAliyun(Describe):
    def __init__(
            self,
            client,
            des_request,
            response_filed: str,
            child_response_filed: str = None,
            parser_response_func: callable = aliyun_parser_response
    ):
        self.client = client
        self.des_request = des_request
        self.response_filed = response_filed
        self.child_response_filed = child_response_filed
        self.parser_response_func = parser_response_func

    def parser_response(self):
        return self.parser_response_func(self.describe(), self.response_filed, self.child_response_filed)

    def describe(self):
        return getattr(self.client, 'do_action_with_exception')(self.des_request)


class DescribeAws(Describe):
    def __init__(
            self,
            client,
            des_request: str,
            response_field: str,
            child_response_filed: str = None,
            des_request_kwargs: dict = None,
            parser_response_func: callable = aws_parser_response
    ):
        self.client = client
        self.des_request = des_request
        self.des_request_kwargs = dict() if des_request_kwargs is None else des_request_kwargs
        self.response_field = response_field
        self.child_response_filed = child_response_filed
        self.parser_response_func = parser_response_func

    def parser_response(self):
        return self.parser_response_func(self.describe(), self.response_field, self.child_response_filed)

    def describe(self):
        return getattr(self.client, self.des_request)(**self.des_request_kwargs)


class Asset(metaclass=abc.ABCMeta):
    _platform: str = ''

    _table_name: str = None
    _asset_columns: List[AssetColumn] = None
    _is_hump_underline: bool = True
    _table_args: tuple = tuple()
    _table_kwargs: dict = None
    _default_columns = [
        AssetColumn(name='account_id', type='str', len=128, kwargs={'nullable': False, 'default': ''}),
        AssetColumn(name='region', type='str', len=128, kwargs={'nullable': False, 'default': ''}),
        AssetColumn(
            name='record_date', type='date',
            kwargs={'nullable': False, 'default': datetime.datetime.now, 'onupdate': datetime.datetime.now}
        )
    ]
    _field_document: str = ''

    def __init__(
            self, cred, region=None, dbconfig: DbConfig = None, parser_response: callable = None
    ):
        self.cred = cred
        self.region = region
        self.dbconfig = dbconfig
        self._engine = create_engine(
            "postgresql://{user}:{password}@{host}:{port}/{database}".format(**self.dbconfig.dict())
        )
        if not self._table_name.startswith(f'{self._platform}_'):
            self._table_name = f'{self._platform}_{self._table_name}'
        self.asset_table = AssetTable(
            self._table_name, self._engine, self._asset_columns,
            default_columns=self._default_columns,
            is_hump_underline=self._is_hump_underline,
            args=self._table_args,
            kwargs=self._table_kwargs
        )
        self.parser_response = parser_response
        self._account_id = self._get_account_id()
        for default_column in self._default_columns:
            if default_column.name == 'account_id':
                default_column.kwargs['default'] = self.account_id
            if default_column.name == 'region':
                default_column.kwargs['default'] = self.region

    @property
    def engine(self):
        return self._engine

    @property
    def table(self) -> Table:
        return self.asset_table.table

    @property
    def assets(self) -> list:
        return self._get_assets()

    @property
    def paginate_all_assets(self) -> list:
        return self._paginate_all_assets()

    @property
    def client(self):
        return self._get_client()

    @property
    def account_id(self):
        return self._account_id

    def _paginate_all_assets(self) -> list:
        raise NotImplementedError("")

    def _get_assets(self) -> list:
        raise NotImplementedError("")

    def _get_client(self):
        raise NotImplementedError("")

    def _get_account_id(self):
        raise NotImplementedError("")

    def fetch(self):

        if self._is_hump_underline:
            paginate_all_assets = self.assets_to_hump_underline(self.paginate_all_assets, self.asset_table.columns)
        else:
            paginate_all_assets = self.paginate_all_assets

        # all_assets datetime, bool, ... to str
        paginate_all_assets = recursive_list(paginate_all_assets)
        if paginate_all_assets:
            uc = [_ for _ in self._table_args if isinstance(_, UniqueConstraint)]
            if uc:
                AssetTable.insert_values_duplicat_do_nothing(self.table, paginate_all_assets, self.engine, uc[0].name)
            else:
                AssetTable.insert_values(self.table, paginate_all_assets, self.engine)
        return True

    @classmethod
    def assets_to_hump_underline(cls, assets: List[dict], asset_columns: List[AssetColumn]) -> List[dict]:
        _assets, asset_columns = [], [asset_column.name for asset_column in asset_columns]

        for asset in assets:
            _ = copy.deepcopy(asset)
            _asset = {}
            _asset_keys = {to_hump_underline(key): key for key in _.keys()}
            for asset_column in asset_columns:
                if asset_column not in _asset_keys:
                    if asset_column in ('account_id', 'record_date', 'region'):
                        continue
                    _asset.update({asset_column: None})
                else:
                    _asset[asset_column] = asset.pop(_asset_keys[asset_column])
            _assets.append(_asset)

        return _assets

    @classmethod
    def load_creds(cls, profile):
        raise NotImplementedError("")


class TencentAsset(Asset):
    _platform = 'tencent'

    _describe = DescribeTencent
    _des_request_func: str = ''
    _des_request: object = None
    _response_field: str = ''

    _paginate_type = 'int'  # int or str

    def __init__(
            self,
            cred: STSAssumeRoleCredential,
            region=None,
            dbconfig: DbConfig = None,
            parser_response: callable = tencent_parser_response
    ):
        super(TencentAsset, self).__init__(cred, region=region, dbconfig=dbconfig, parser_response=parser_response)
        self.asset_describe = self._describe(
            self.client, self._des_request_func, self._des_request, self._response_field)

    def _get_assets(self):
        return self.asset_describe.parser_response()

    def _paginate_all_assets(self):
        page, assets = 0, []
        _des_request = copy.deepcopy(self._des_request)
        _des_request.Limit = 50 if self._paginate_type == 'int' else '50'

        while True:
            response = self._describe(
                self.client, self._des_request_func, _des_request, self._response_field).parser_response()
            if not response:
                break

            assets += response
            page = 1
            if isinstance(_des_request.Limit, str):
                _des_request.Offset = str(page * int(_des_request.Limit))
            else:
                _des_request.Offset = page * _des_request.Limit
        return assets

    def _get_client(self):
        pass

    def _get_account_id(self):
        return get_tencent_account_id(self.cred)

    @classmethod
    def load_creds(cls, profile: TencentProfile) -> List[STSAssumeRoleCredential]:
        return [
            STSAssumeRoleCredential(
                profile.ak,
                profile.sk,
                role.arn,
                role.session_name,
                duration_seconds=role.duration_seconds
            ) for role in profile.roles
        ]


class AliyunAsset(Asset):
    _platform = 'aliyun'

    _des_request: callable = None
    _response_field = ''
    _child_response_filed = None

    _describe = DescribeAliyun

    def __init__(
            self,
            cred: RamRoleArnCredential,
            region: str = None,
            dbconfig: DbConfig = None,
            parser_response: callable = aliyun_parser_response
    ):
        super(AliyunAsset, self).__init__(cred, region=region, dbconfig=dbconfig, parser_response=parser_response)
        self._des_request = self._des_request()
        self._des_request.set_accept_format('json')
        """
                    client,
            des_request,
            response_filed: str,
            parser_response_func: callable = aliyun_parser_response
        """
        self.asset_describe = self._describe(
            self.client,
            self._des_request,
            self._response_field,
            self._child_response_filed,
            self.parser_response
        )

    def _paginate_all_assets(self):
        page, page_size, assets = 0, 50, []
        self._des_request.set_PageSize(page_size)
        while True:
            response = self._describe(
                self.client,
                self._des_request,
                self._response_field,
                self._child_response_filed,
                self.parser_response
            ).parser_response()
            if not response:
                break

            assets += response
            page += 1
            self._des_request.set_PageNumber(page*page_size)
        print(assets)
        return assets

    def _get_client(self):
        """由子类实现"""
        pass

    def _get_assets(self):
        return self.asset_describe.parser_response()

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


class AwsAsset(Asset):
    _platform = 'aws'

    _client_name: str = ''
    _des_request: str = ''
    _response_field: str = ''
    _child_response_filed: str = None
    _des_request_kwargs: dict = {'MaxResults': 50}
    _next_type = 'NextToken'

    _describe = DescribeAws

    def __init__(
            self,
            cred: AwsCredential,
            region=None,
            dbconfig: DbConfig = None,
            parser_response: callable = aws_parser_response
    ):
        super(AwsAsset, self).__init__(cred, region=region, dbconfig=dbconfig, parser_response=parser_response)
        self.asset_describe = self._describe(
            self.client,
            self._des_request,
            self._response_field,
            des_request_kwargs=self._des_request_kwargs,
            parser_response_func=parser_response
        )

    def _paginate_all_assets(self) -> list:
        assets = []
        _des_request_kwargs = copy.deepcopy(self._des_request_kwargs)
        while True:
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

    def _get_client(self):
        """由子类实现"""
        return Session(**self.cred.dict()).client(self._client_name, region_name=self.region)

    def _get_assets(self) -> list:
        assets, _ = self.asset_describe.parser_response()
        return assets

    def _get_account_id(self):
        return get_aws_account_id(self.cred)

    @classmethod
    def load_creds(cls, profile: AwsProfile) -> List[AwsCredential]:
        for role in profile.roles:
            yield aws_assume_role(role.arn, role_session_name=role.session_name, duration_seconds=role.duration_seconds)