# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.aws.cloudwatch import Ec2CpuUtilization
from asset.test.config import aws_cred, db_config

import datetime
import boto3

if __name__ == '__main__':
    # print(Ec2CpuUtilization(cred=aws_cred, region='cn-northwest-1', dbconfig=db_config).paginate_all_assets)
    a = {
        "Id": "m1",
        "MetricStat": {
            "Metric": {
                "Namespace": "AWS/EC2",
                "MetricName": "CPUUtilization",
                "Dimensions": [
                    {
                        "Name": "InstanceId",
                        "Value": "i-0bf03669fc5c6da52"
                    }
                ]
            },
            "Period": 3600,
            "Stat": "Minimum"
        }
    }
    d = {
        'Id': 'm1',
        'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/EC2',
                'MetricName': 'CPUUtilization',
                'Dimensions': [
                    {
                        "Name": "InstanceId",
                        "Value": "i-0bf03669fc5c6da52"
                    }
                ]
            },
            'Period': 3600,
            'Stat': 'Minimum',
            'Unit': 'Second'
        },
    }
    cli = boto3.client('cloudwatch', **aws_cred.dict(), region_name='cn-north-1')
    b = cli.get_metric_data(
        MetricDataQueries=[d],
        StartTime=datetime.datetime(2023, 1, 7),
        EndTime=datetime.datetime(2023, 1, 8),
        MaxDatapoints=123
    )
    print(b)
