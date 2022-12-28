# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aliyun.ecs import Ecs
from asset.test.base_config import Aliyun
from aliyunsdkcore.auth.credentials import RamRoleArnCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


def get_assets():
    for role in Aliyun.profile.roles:
        for region in role.regions:
            ecs = Ecs(
                cred=RamRoleArnCredential(Aliyun.profile.ak, Aliyun.profile.sk, role.arn, role.session_name),
                region=region,
                dbconfig=Aliyun.dbconfig
            )
            # print(ecs.account_id)
            # print(ecs.assets)
            # print(ecs.paginate_all_assets)
            ecs.fetch()


if __name__ == '__main__':
    get_assets()
