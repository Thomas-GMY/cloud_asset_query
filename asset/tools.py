# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

import datetime


def asset_columns_generator(fields: dict):
    _fields = []
    for key, value in fields.items():
        if isinstance(value, str) or isinstance(value, bool):
            _type = 'str'
        elif isinstance(value, int):
            _type = 'int'
        elif isinstance(value, dict) or isinstance(value, list):
            _type = 'dict'
        elif isinstance(value, datetime.date):
            _type = 'date'
        elif isinstance(value, datetime.datetime):
            _type = 'datetime'
        elif isinstance(value, float):
            _type = 'float'
        else:
            raise Exception(f'不支持的类型, value: {value}')
        _fields.append({'name': key, 'type': _type})
    return _fields


if __name__ == '__main__':

    fields_demo =    {
      "CreationTime": "2019-12-25T12:31:31Z",
      "VpcId": "vpc-bp1j7w3gc1cexjqd****",
      "Type": "Secondary",
      "Status": "Available",
      "NetworkInterfaceTrafficMode": "Standard",
      "NetworkInterfaceName": "my-eni-name",
      "MacAddress": "00:16:3e:12:**:**",
      "QueuePairNumber": 0,
      "NetworkInterfaceId": "eni-bp125p95hhdhn3ot****",
      "ServiceID": 12345678910,
      "InstanceId": "i-bp1e2l6djkndyuli****",
      "OwnerId": "123456****",
      "ServiceManaged": 'true',
      "VSwitchId": "vsw-bp16usj2p27htro3****",
      "Description": "DescriptionTest",
      "ResourceGroupId": "rg-2ze88m67qx5z****",
      "ZoneId": "cn-hangzhou-e",
      "PrivateIpAddress": "172.17.**.**",
      "QueueNumber": 8,
      "PrivateIpSets": [
        {
          "PrivateIpAddress": "172.17.**.**",
          "Primary": 'true',
          "AssociatedPublicIp": {
            "PublicIpAddress": "116.62.**.**",
            "AllocationId": "null"
          }
        }
      ],
      "Ipv6Sets": [
        {
          "Ipv6Address": "2408:4321:180:1701:94c7:bc38:3bfa:****"
        }
      ],
      "Ipv4PrefixSets": [
        {
          "Ipv4Prefix": "hide"
        }
      ],
      "Ipv6PrefixSets": [
        {
          "Ipv6Prefix": "hide"
        }
      ],
      "Tags": [
        {
          "TagValue": "TestValue",
          "TagKey": "TestKey"
        }
      ],
      "SecurityGroupIds": [
        "sg-bp18kz60mefsicfg****"
      ],
      "AssociatedPublicIp": {
        "PublicIpAddress": "116.62.**.**",
        "AllocationId": "null"
      },
      "Attachment": {
        "DeviceIndex": 0,
        "InstanceId": "null",
        "TrunkNetworkInterfaceId": "null",
        "NetworkCardIndex": 0
      }
    }
    for asset in asset_columns_generator(fields=fields_demo):
        print(str(asset) + ',')