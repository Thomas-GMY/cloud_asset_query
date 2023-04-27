# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import HuaweiAsset, AssetColumn, UniqueConstraint
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkevs.v2.region.evs_region import EvsRegion
from huaweicloudsdkeip.v2.region.eip_region import EipRegion
from huaweicloudsdknat.v2.region.nat_region import NatRegion

from huaweicloudsdkecs.v2.ecs_client import EcsClient
from huaweicloudsdkecs.v2.model import ListServersDetailsRequest

from huaweicloudsdkevs.v2.evs_client import EvsClient
from huaweicloudsdkevs.v2.model import ListVolumesRequest

from huaweicloudsdkeip.v2.eip_client import EipClient
from huaweicloudsdkeip.v2.model import ListPublicipsRequest

from huaweicloudsdknat.v2.nat_client import NatClient
from huaweicloudsdknat.v2.model import ListNatGatewaysRequest


ecs_asset_columns = [
    {'name': 'tenant_id', 'type': 'str'},
    {'name': 'metadata', 'type': 'dict'},
    {'name': 'addresses', 'type': 'dict'},
    {'name': 'OS-EXT-STS:task_state', 'type': 'str'},
    {'name': 'OS-DCF:diskConfig', 'type': 'str'},
    {'name': 'OS-EXT-AZ:availability_zone', 'type': 'str'},
    {'name': 'links', 'type': 'dict'},
    {'name': 'OS-EXT-STS:power_state', 'type': 'int'},
    {'name': 'id', 'type': 'str'},
    {'name': 'os-extended-volumes:volumes_attached', 'type': 'dict'},
    {'name': 'OS-EXT-SRV-ATTR:host', 'type': 'str'},
    {'name': 'accessIPv4', 'type': 'str'},
    {'name': 'image', 'type': 'dict'},
    {'name': 'OS-SRV-USG:terminated_at', 'type': 'str'},
    {'name': 'accessIPv6', 'type': 'str'},
    {'name': 'created', 'type': 'str'},
    {'name': 'hostId', 'type': 'str'},
    {'name': 'OS-EXT-SRV-ATTR:hypervisor_hostname', 'type': 'str'},
    {'name': 'flavor', 'type': 'dict'},
    {'name': 'key_name', 'type': 'str'},
    {'name': 'security_groups', 'type': 'dict'},
    {'name': 'config_drive', 'type': 'str'},
    {'name': 'OS-EXT-STS:vm_state', 'type': 'str'},
    {'name': 'user_id', 'type': 'str'},
    {'name': 'OS-EXT-SRV-ATTR:instance_name', 'type': 'str'},
    {'name': 'name', 'type': 'str'},
    {'name': 'OS-SRV-USG:launched_at', 'type': 'str'},
    {'name': 'updated', 'type': 'str'},
    {'name': 'status', 'type': 'str'}
]
evs_asset_columns = [
    {'name': 'attachments', 'type': 'dict'},
    {'name': 'availability_zone', 'type': 'str'},
    {'name': 'bootable', 'type': 'str'},
    {'name': 'created_at', 'type': 'str'},
    {'name': 'id', 'type': 'str'},
    {'name': 'links', 'type': 'dict'},
    {'name': 'metadata', 'type': 'dict'},
    {'name': 'name', 'type': 'str'},
    {'name': 'os-vol-host-attr:host', 'type': 'str'},
    {'name': 'volume_image_metadata', 'type': 'dict'},
    {'name': 'os-vol-tenant-attr:tenant_id', 'type': 'str'},
    {'name': 'replication_status', 'type': 'str'},
    {'name': 'multiattach', 'type': 'str'},
    {'name': 'size', 'type': 'int'},
    {'name': 'status', 'type': 'str'},
    {'name': 'updated_at', 'type': 'str'},
    {'name': 'user_id', 'type': 'str'},
    {'name': 'volume_type', 'type': 'str'},
    {'name': 'service_type', 'type': 'str'},
    {'name': 'wwn', 'type': 'str'}
]
eip_asset_columns = [
    {'name': 'tenant_id', 'type': 'str'},
    {'name': 'bandwidth_name', 'type': 'str'},
    {'name': 'public_ip_address', 'type': 'str'},
    {'name': 'create_time', 'type': 'str'},
    {'name': 'profile', 'type': 'dict'},
    {'name': 'type', 'type': 'str'},
    {'name': 'bandwidth_id', 'type': 'str'},
    {'name': 'bandwidth_size', 'type': 'int'},
    {'name': 'enterprise_project_id', 'type': 'str'},
    {'name': 'ip_version', 'type': 'int'},
    {'name': 'private_ip_address', 'type': 'str'},
    {'name': 'bandwidth_share_type', 'type': 'str'},
    {'name': 'id', 'type': 'str'},
    {'name': 'status', 'type': 'str'},
    {'name': 'port_id', 'type': 'str'},
    {'name': 'public_border_group', 'type': 'str'},
    {'name': 'allow_share_bandwidth_types', 'type': 'dict'}
]
nat_asset_columns = [
    {'name': 'id', 'type': 'str'},
    {'name': 'router_id', 'type': 'str'},
    {'name': 'status', 'type': 'str'},
    {'name': 'description', 'type': 'str'},
    {'name': 'admin_state_up', 'type': 'str'},
    {'name': 'tenant_id', 'type': 'str'},
    {'name': 'created_at', 'type': 'str'},
    {'name': 'spec', 'type': 'str'},
    {'name': 'internal_network_id', 'type': 'str'},
    {'name': 'name', 'type': 'str'},
    {'name': 'enterprise_project_id', 'type': 'str'}
]

ecs_field_document = 'https://support.huaweicloud.com/api-ecs/ecs_05_0002.html'
evs_field_document = 'https://support.huaweicloud.com/api-evs/evs_04_2006.html'
eip_field_document = 'https://support.huaweicloud.com/api-eip/eip_api_0002.html'
nat_field_document = 'https://support.huaweicloud.com/api-natgateway/ListNatGateways.html'


@cloud_providers.huawei.register('ecs')
class Ecs(HuaweiAsset):

    _client = EcsClient
    _region_obj = EcsRegion
    _des = 'list_servers_details'
    _request_obj = ListServersDetailsRequest
    _response_field = 'servers'

    _table_name = 'huawei_ecs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in ecs_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'id', name='huawei_uc_ecs'),)
    _field_document = ecs_field_document


@cloud_providers.huawei.register('evs')
class Evs(HuaweiAsset):
    _client = EvsClient
    _region_obj = EvsRegion
    _des = 'list_volumes'
    _request_obj = ListVolumesRequest
    _response_field = 'volumes'

    _table_name = 'huawei_evs'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in evs_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'id', name='huawei_uc_evs'),)
    _field_document = evs_field_document


@cloud_providers.huawei.register('eip')
class Eip(HuaweiAsset):
    _client = EipClient
    _region_obj = EipRegion
    _des = 'list_publicips'
    _request_obj = ListPublicipsRequest
    _response_field = 'publicips'
    _request_pars = {'limit': 2000}
    _offset = False

    _table_name = 'huawei_eip'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in eip_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'id', name='huawei_uc_eip'),)
    _field_document = eip_field_document


@cloud_providers.huawei.register('nat')
class Nat(HuaweiAsset):
    _client = NatClient
    _region_obj = NatRegion
    _des = 'list_nat_gateways'
    _request_obj = ListNatGatewaysRequest
    _response_field = 'nat_gateways'
    _request_pars = {'limit': 2000}
    _offset = False

    _table_name = 'huawei_nat'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in nat_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'id', name='huawei_uc_nat'),)
    _field_document = nat_field_document

