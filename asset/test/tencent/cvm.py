# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.commands import FetchTencent
from asset.tencent.cvm import Cvm
from asset.test.base_config import Tencent
from tencentcloud.common.credential import STSAssumeRoleCredential


def get_assets():
    for role in Tencent.profile.roles:
        for region in role.regions:
            cred = STSAssumeRoleCredential(
                Tencent.profile.ak, Tencent.profile.sk, role.arn, role.session_name, role.duration_seconds)
            # print(Cvm(cred, region=region, dbconfig=Tencent.dbconfig).assets_to_json_string)
            # print(Cvm(cred, region=region, dbconfig=Tencent.dbconfig).assets)
            print(Cvm(cred, region=region, dbconfig=Tencent.dbconfig).paginate_all_assets)


def fetch():
    fetch_tencent = FetchTencent(profile=Tencent.profile, dbconfig=Tencent.dbconfig)
    fetch_tencent.fetch()


if __name__ == '__main__':
    get_assets()
