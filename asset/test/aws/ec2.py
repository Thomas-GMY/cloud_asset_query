# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aws.ec2 import Ec2
from asset.test.config import aws_cred, db_config


ec2_assets = Ec2(cred=aws_cred, region='cn-northwest-1', dbconfig=db_config)


if __name__ == '__main__':
    # print(ec2_assets.paginate_all_assets)
    ec2_assets.fetch()