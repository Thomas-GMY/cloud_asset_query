# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint

alternate_contact_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_alternate_contact.html'
contact_information_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account/client/get_contact_information.html'

alternate_contact_columns = [
    {'name': 'AlternateContactType', 'type': 'str'},
    {'name': 'EmailAddress', 'type': 'str'},
    {'name': 'Name', 'type': 'str'},
    {'name': 'PhoneNumber', 'type': 'str'},
    {'name': 'Title', 'type': 'str'}
]
contact_information_columns = [
    {'name': 'AddressLine1', 'type': 'str'},
    {'name': 'AddressLine2', 'type': 'str'},
    {'name': 'AddressLine3', 'type': 'str'},
    {'name': 'City', 'type': 'str'},
    {'name': 'CompanyName', 'type': 'str'},
    {'name': 'CountryCode', 'type': 'str'},
    {'name': 'DistrictOrCounty', 'type': 'str'},
    {'name': 'FullName', 'type': 'str'},
    {'name': 'PhoneNumber', 'type': 'str'},
    {'name': 'PostalCode', 'type': 'str'},
    {'name': 'StateOrRegion', 'type': 'str'},
    {'name': 'WebsiteUrl', 'type': 'str'}
]


@cloud_providers.aws.register('contact_information')
class ContactInformation(AwsAsset):
    _client_name = 'account'
    _des_request = 'get_contact_information'
    _response_field = 'ContactInformation'

    _des_request_kwargs = {}

    _table_name = 'aws_contact_information'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in contact_information_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'phone_number', name='aws_uc_account_ci'),)
    _field_document = contact_information_field_document


@cloud_providers.aws.register('alternate_contact')
class AlternateContact(AwsAsset):
    _client_name = 'account'
    _des_request = 'get_alternate_contact'
    _response_field = 'AlternateContact'
    _des_request_kwargs = {'AlternateContactType': 'OPERATIONS'}

    _table_name = 'aws_alternate_contact'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in alternate_contact_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'phone_number', name='aws_uc_account_ac'),)
    _field_document = alternate_contact_field_document
