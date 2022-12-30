from asset.aws.ec2 import Ec2
from asset.utils import aws_assume_role

arn = 'arn:aws-cn:iam::247987438980:role/asset_fetch_for_test'
cred = aws_assume_role(ak=ak, sk=sk, arn=arn)

if __name__ == '__main__':
    print(cred)