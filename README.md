## Cloud Asset Query

云资产（云资源）采集到postgresql，支持的云代理商包括（腾讯云、阿里云、AWS），并支持通过role多账号方式采集

----
**安装**
    
    pip install cloud-asset


**命令格式**

    cloud-asset [fetch] [--cloud-provider] [--profile-path] [--assets] [--regions] [--log-dir-path]

*参数详情*
- --cloud-provider: 支持的云厂商(aws、aliyun、tencent)
- --profile-path: 配置文件路径，采用assume role的方式去获取资产(即使是同一个账号、也需要通过ak/sk去assume role)，这里需要注意，Aws的ak/sk不需要在profile设置
只需要根据boto3设置即可(只需要填写role的arn即可)、有不明白可以email到gmy.big.father@gmail.com。
- --assets: 需要采集的云资产，具体资产列表请查看具体云厂商，支持多个资产一起采集，格式为xxx,xxx需要以,号分开。（默认为all，表示去采集该云厂商下以支持的全部云资产）
- --regions: 表示采集该region下面的资产，支持多个region一起采集，格式为xxx,xxx需要以,号分开(默认为all,去采集所有region)
- --log-dir-path: 输出的日志文件存储路径

----

### AWS
**command demo**

    cloud-asset fetch --cloud-provider aws --profile-path xxx.yaml --assets ec2,security_groups --regions cn-northwest-1

##### 支持的云资产列表，基于boto3(1.26.29)

| 资产                  | 描述                       | 字段文档                                                                                                                               |
|---------------------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| ec2                 | ec2                      | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data) |
| ec2_cpu_utilization | ec2的cpu利用率               | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data)|                                                                                                                             |                                                                                                                                 |
| security_groups     | 安全组                      | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets)|                                                                                                                             |                                                                                                                                 |
| vpc                 | vpc                      | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs)|                                                                                                                             |                                                                                                                                 |
| subnets             | subnets                  | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets)|                                                                                                                             |                                                                                                                                 |
| network_interfaces  | network_interfaces       | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces)|                                                                                                                             |                                                                                                                                 |
| s3_buckets          | 对象存储                     | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets)|                                                                                                                             |                                                                                                                                 |
| rds_db_instances    | rds_db_instances         | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances)|                                                                                                                             |                                                                                                                                 |
| rds_db_clusters     | rds_db_clusters          | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_clusters)|                                                                                                                             |                                                                                                                                 |
| elb                 | 老版本的elb                  | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.describe_load_balancers)|                                                                                                                             |                                                                                                                                 |
| elb_v2              | 新版本的elb                  | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers)|                                                                                                                             |                                                                                                                                 |
| elb_v2_listeners    | 新版本的elb监听器               | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_listeners)|                                                                                                                             |                                                                                                                                 |
| elb_v2_target_groups    | 新版本的elb目标组               | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups)|                                                                                                                             |                                                                                                                                 |
| elb_v2_target_group_health  | 新版本的elb目标组后的状态(查看后面挂的资源) | [go](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health)|                                                                                                                             |                                                                                                                                 |

----


### 腾讯云
**command demo**

    cloud-asset fetch --cloud-provider tencent --profile-path xxx.yaml --assets cvm,cos --regions ap-shanghai

##### 支持的云资产列表，基于tencentcloud-sdk-python(3.0.773), cos-python-sdk-v5(1.9.22)
| 资产                 | 描述          | 字段文档                                                                                                                             |
|--------------------|-------------|--------------------------------------------------------|
| cvm                | cvm(虚机)     | [go](https://cloud.tencent.com/document/api/213/15728)|
| cvm_cpu_usage      | 虚机cpu利用率    | [go](https://cloud.tencent.com/document/api/248/31014)|
| vpcs               | vpc         | [go](https://cloud.tencent.com/document/api/215/15778)|
| subnets            | subnets(子网) | [go](https://cloud.tencent.com/document/api/215/15784)|
| route_tables       | 路由表         | [go](https://cloud.tencent.com/document/api/215/15763)|
| eips               | 弹性公网IP      | [go](https://cloud.tencent.com/document/api/215/16702)|
| network_interfaces | 网络接口        | [go](https://cloud.tencent.com/document/api/215/15817)|
| nats               | Nat 网关      | [go](https://cloud.tencent.com/document/api/215/36034)|
| cdb_mysql          | cdb（Mysql）  | [go](https://cloud.tencent.com/document/api/236/15872#1.-.E6.8E.A5.E5.8F.A3.E6.8F.8F.E8.BF.B0)|
| cos                | cos（对象存储）   | [go](https://cloud.tencent.com/document/api/236/15872#1.-.E6.8E.A5.E5.8F.A3.E6.8F.8F.E8.BF.B0)|
| clb                | 负载均衡        | [go](https://cloud.tencent.com/document/api/214/30685)|


### 阿里云
**command demo**

    cloud-asset fetch --cloud-provider aliyun --profile-path xxx.yaml --assets ecs
##### 支持的云资产列表
| 资产  | 描述      | 字段文档                                                                                                                             |
|-----|---------|--------------------------------------------------------|
| ecs | ecs(虚机) | [go](ecs_field_document)|
    