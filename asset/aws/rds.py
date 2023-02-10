# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0

from asset.asset_register import cloud_providers
from asset.base import AwsAsset, AssetColumn, UniqueConstraint


db_instances_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances'
db_clusters_field_document = 'https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_clusters'

db_instances_asset_columns = [
    {'name': 'DBInstanceIdentifier', 'type': 'str'},
    {'name': 'DBInstanceClass', 'type': 'str'},
    {'name': 'Engine', 'type': 'str'},
    {'name': 'DBInstanceStatus', 'type': 'str'},
    {'name': 'AutomaticRestartTime', 'type': 'datetime'},
    {'name': 'MasterUsername', 'type': 'str'},
    {'name': 'DBName', 'type': 'str'},
    {'name': 'Endpoint', 'type': 'dict'},
    {'name': 'AllocatedStorage', 'type': 'int'},
    {'name': 'InstanceCreateTime', 'type': 'datetime'},
    {'name': 'PreferredBackupWindow', 'type': 'str'},
    {'name': 'BackupRetentionPeriod', 'type': 'int'},
    {'name': 'DBSecurityGroups', 'type': 'dict'},
    {'name': 'VpcSecurityGroups', 'type': 'dict'},
    {'name': 'DBParameterGroups', 'type': 'dict'},
    {'name': 'AvailabilityZone', 'type': 'str'},
    {'name': 'DBSubnetGroup', 'type': 'dict'},
    {'name': 'PreferredMaintenanceWindow', 'type': 'str'},
    {'name': 'PendingModifiedValues', 'type': 'dict'},
    {'name': 'LatestRestorableTime', 'type': 'datetime'},
    {'name': 'MultiAZ', 'type': 'bool'},
    {'name': 'EngineVersion', 'type': 'str'},
    {'name': 'AutoMinorVersionUpgrade', 'type': 'bool'},
    {'name': 'ReadReplicaSourceDBInstanceIdentifier', 'type': 'str'},
    {'name': 'ReadReplicaDBInstanceIdentifiers', 'type': 'dict'},
    {'name': 'ReplicaMode', 'type': 'str'},
    {'name': 'LicenseModel', 'type': 'str'},
    {'name': 'Iops', 'type': 'int'},
    {'name': 'OptionGroupMemberships', 'type': 'dict'},
    {'name': 'CharacterSetName', 'type': 'str'},
    {'name': 'NcharCharacterSetName', 'type': 'str'},
    {'name': 'SecondaryAvailabilityZone', 'type': 'str'},
    {'name': 'PubliclyAccessible', 'type': 'bool'},
    {'name': 'StatusInfos', 'type': 'dict'},
    {'name': 'StorageType', 'type': 'str'},
    {'name': 'TdeCredentialArn', 'type': 'str'},
    {'name': 'DbInstancePort', 'type': 'int'},
    {'name': 'DBClusterIdentifier', 'type': 'str'},
    {'name': 'StorageEncrypted', 'type': 'bool'},
    {'name': 'KmsKeyId', 'type': 'str'},
    {'name': 'DbiResourceId', 'type': 'str'},
    {'name': 'CACertificateIdentifier', 'type': 'str'},
    {'name': 'DomainMemberships', 'type': 'dict'},
    {'name': 'CopyTagsToSnapshot', 'type': 'bool'},
    {'name': 'MonitoringInterval', 'type': 'int'},
    {'name': 'EnhancedMonitoringResourceArn', 'type': 'str'},
    {'name': 'MonitoringRoleArn', 'type': 'str'},
    {'name': 'PromotionTier', 'type': 'int'},
    {'name': 'DBInstanceArn', 'type': 'str'},
    {'name': 'Timezone', 'type': 'str'},
    {'name': 'IAMDatabaseAuthenticationEnabled', 'type': 'bool'},
    {'name': 'PerformanceInsightsEnabled', 'type': 'bool'},
    {'name': 'PerformanceInsightsKMSKeyId', 'type': 'str'},
    {'name': 'PerformanceInsightsRetentionPeriod', 'type': 'int'},
    {'name': 'EnabledCloudwatchLogsExports', 'type': 'dict'},
    {'name': 'ProcessorFeatures', 'type': 'dict'},
    {'name': 'DeletionProtection', 'type': 'bool'},
    {'name': 'AssociatedRoles', 'type': 'dict'},
    {'name': 'ListenerEndpoint', 'type': 'dict'},
    {'name': 'MaxAllocatedStorage', 'type': 'int'},
    {'name': 'TagList', 'type': 'dict'},
    {'name': 'DBInstanceAutomatedBackupsReplications', 'type': 'dict'},
    {'name': 'CustomerOwnedIpEnabled', 'type': 'bool'},
    {'name': 'AwsBackupRecoveryPointArn', 'type': 'str'},
    {'name': 'ActivityStreamStatus', 'type': 'str'},
    {'name': 'ActivityStreamKmsKeyId', 'type': 'str'},
    {'name': 'ActivityStreamKinesisStreamName', 'type': 'str'},
    {'name': 'ActivityStreamMode', 'type': 'str'},
    {'name': 'ActivityStreamEngineNativeAuditFieldsIncluded', 'type': 'bool'},
    {'name': 'AutomationMode', 'type': 'str'},
    {'name': 'ResumeFullAutomationModeTime', 'type': 'datetime'},
    {'name': 'CustomIamInstanceProfile', 'type': 'str'},
    {'name': 'BackupTarget', 'type': 'str'},
    {'name': 'NetworkType', 'type': 'str'},
    {'name': 'ActivityStreamPolicyStatus', 'type': 'str'},
    {'name': 'StorageThroughput', 'type': 'int'},
    {'name': 'DBSystemId', 'type': 'str'},
    {'name': 'MasterUserSecret', 'type': 'dict'},
    {'name': 'CertificateDetails', 'type': 'dict'}
]
db_clusters_asset_columns = [
    {'name': 'AllocatedStorage', 'type': 'str'},
    {'name': 'AvailabilityZones', 'type': 'dict'},
    {'name': 'BackupRetentionPeriod', 'type': 'int'},
    {'name': 'CharacterSetName', 'type': 'str'},
    {'name': 'DatabaseName', 'type': 'str'},
    {'name': 'DBClusterIdentifier', 'type': 'str'},
    {'name': 'DBClusterParameterGroup', 'type': 'str'},
    {'name': 'DBSubnetGroup', 'type': 'str'},
    {'name': 'Status', 'type': 'str'},
    {'name': 'AutomaticRestartTime', 'type': 'datetime'},
    {'name': 'PercentProgress', 'type': 'str'},
    {'name': 'EarliestRestorableTime', 'type': 'datetime'},
    {'name': 'Endpoint', 'type': 'str'},
    {'name': 'ReaderEndpoint', 'type': 'str'},
    {'name': 'CustomEndpoints', 'type': 'dict'},
    {'name': 'MultiAZ', 'type': 'bool'},
    {'name': 'Engine', 'type': 'str'},
    {'name': 'EngineVersion', 'type': 'str'},
    {'name': 'LatestRestorableTime', 'type': 'dict'},
    {'name': 'Port', 'type': 'int'},
    {'name': 'MasterUsername', 'type': 'str'},
    {'name': 'DBClusterOptionGroupMemberships', 'type': 'dict'},
    {'name': 'PreferredBackupWindow', 'type': 'str'},
    {'name': 'PreferredMaintenanceWindow', 'type': 'str'},
    {'name': 'ReplicationSourceIdentifier', 'type': 'str'},
    {'name': 'ReadReplicaIdentifiers', 'type': 'dict'},
    {'name': 'DBClusterMembers', 'type': 'dict'},
    {'name': 'VpcSecurityGroups', 'type': 'dict'},
    {'name': 'HostedZoneId', 'type': 'str'},
    {'name': 'StorageEncrypted', 'type': 'bool'},
    {'name': 'KmsKeyId', 'type': 'str'},
    {'name': 'DbClusterResourceId', 'type': 'bool'},
    {'name': 'DBClusterArn', 'type': 'str'},
    {'name': 'AssociatedRoles', 'type': 'dict'},
    {'name': 'IAMDatabaseAuthenticationEnabled', 'type': 'bool'},
    {'name': 'CloneGroupId', 'type': 'str'},
    {'name': 'ClusterCreateTime', 'type': 'datetime'},
    {'name': 'EarliestBacktrackTime', 'type': 'datetime'},
    {'name': 'BacktrackWindow', 'type': 'int'},
    {'name': 'BacktrackConsumedChangeRecords', 'type': 'int'},
    {'name': 'EnabledCloudwatchLogsExports', 'type': 'dict'},
    {'name': 'Capacity', 'type': 'int'},
    {'name': 'EngineMode', 'type': 'str'},
    {'name': 'ScalingConfigurationInfo', 'type': 'dict'},
    {'name': 'DeletionProtection', 'type': 'bool'},
    {'name': 'HttpEndpointEnabled', 'type': 'bool'},
    {'name': 'ActivityStreamMode', 'type': 'str'},
    {'name': 'ActivityStreamStatus', 'type': 'str'},
    {'name': 'ActivityStreamKmsKeyId', 'type': 'str'},
    {'name': 'ActivityStreamKinesisStreamName', 'type': 'str'},
    {'name': 'CopyTagsToSnapshot', 'type': 'bool'},
    {'name': 'CrossAccountClone', 'type': 'bool'},
    {'name': 'DomainMemberships', 'type': 'dict'},
    {'name': 'TagList', 'type': 'dict'},
    {'name': 'GlobalWriteForwardingStatus', 'type': 'str'},
    {'name': 'GlobalWriteForwardingRequested', 'type': 'bool'},
    {'name': 'PendingModifiedValues', 'type': 'dict'},
    {'name': 'DBClusterInstanceClass', 'type': 'str'},
    {'name': 'StorageType', 'type': 'str'},
    {'name': 'Iops', 'type': 'int'},
    {'name': 'PubliclyAccessible', 'type': 'bool'},
    {'name': 'AutoMinorVersionUpgrade', 'type': 'bool'},
    {'name': 'MonitoringInterval', 'type': 'int'},
    {'name': 'MonitoringRoleArn', 'type': 'str'},
    {'name': 'PerformanceInsightsEnabled', 'type': 'bool'},
    {'name': 'PerformanceInsightsKMSKeyId', 'type': 'str'},
    {'name': 'PerformanceInsightsRetentionPeriod', 'type': 'int'},
    {'name': 'ServerlessV2ScalingConfiguration', 'type': 'dict'},
    {'name': 'NetworkType', 'type': 'str'},
    {'name': 'DBSystemId', 'type': 'str'},
    {'name': 'MasterUserSecret', 'type': 'dict'}
]


@cloud_providers.aws.register('rds_db_instances')
class DbInstances(AwsAsset):
    _client_name = 'rds'
    _des_request = 'describe_db_instances'
    _response_field = 'DBInstances'
    _des_request_kwargs: dict = {'MaxRecords': 100}

    _table_name = 'aws_rds_db_instances'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in db_instances_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'd_b_instance_identifier', name='aws_uc_rds_db_i'),)
    _field_document = db_instances_field_document


@cloud_providers.aws.register('rds_db_clusters')
class DbClusters(AwsAsset):
    _client_name = 'rds'
    _des_request = 'describe_db_clusters'
    _response_field = 'DBClusters'
    _des_request_kwargs: dict = {'MaxRecords': 100}

    _table_name = 'aws_rds_db_clusters'
    _asset_columns = [AssetColumn(**asset_column) for asset_column in db_clusters_asset_columns]
    _table_args = (UniqueConstraint('account_id', 'record_date', 'd_b_cluster_identifier', name='aws_uc_rds_db_c'),)
    _field_document = db_clusters_field_document

