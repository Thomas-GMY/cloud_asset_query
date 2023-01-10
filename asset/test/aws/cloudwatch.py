# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aws.cloudwatch import Ec2CpuUtilization
from asset.test.config import aws_cred, db_config


if __name__ == '__main__':
    print(Ec2CpuUtilization(cred=aws_cred, region='cn-northwest-1', dbconfig=db_config).paginate_all_assets)