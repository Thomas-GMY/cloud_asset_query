# -*- coding: UTF-8 -*-

# Copyright The Cloud Asset Authors.
# SPDX-License-Identifier: Apache-2.0
import copy

from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table, Column

from asset.conf import COLUMNS_MAP
from asset.schema import AssetColumn
from asset.utils import to_hump_underline


class AssetTable:

    def __init__(
            self,
            table_name: str,
            engine: object,
            asset_columns: List[AssetColumn],
            default_columns: List[AssetColumn] = None,
            is_hump_underline: bool = True,
            args: tuple = None,
            kwargs: dict = None
    ):
        """
        :param table_name:
        :param engine:
        :param asset_columns:
        :param default_columns:
        :param is_hump_underline:
        :param args: 创建Table类的*args
        :param kwargs: 创建Table类的**kwargs
        """
        self.asset_columns = self.column_to_hump_underline(asset_columns) if is_hump_underline else asset_columns
        self.asset_columns = list() if default_columns is None else default_columns + self.asset_columns

        self.table_name = table_name
        self.engine = engine

        self.args = tuple() if args is None else args
        self.kwargs = dict() if kwargs is None else kwargs

    @property
    def columns(self):
        return self.generate_columns(self.asset_columns)

    @property
    def table(self) -> Table:
        return self.__create_table()

    def __create_table(self) -> Table:
        table = list(filter(lambda table_name: table_name == self.table_name, self.engine.table_names()))
        if table:
            return Table(self.table_name, MetaData(bind=self.engine), *self.columns, *self.args, **self.kwargs)

        table = Table(self.table_name, MetaData(bind=self.engine), *self.columns, *self.args, **self.kwargs)
        try:
            table.create()
        except Exception as e:
            raise e
        return table

    @classmethod
    def generate_columns(cls, asset_columns: List[AssetColumn]) -> list:
        """把字段转化为下sqlalchemy的columns"""
        columns = []
        for column in asset_columns:
            column_type = COLUMNS_MAP[column.type]
            if column.type == 'str':
                columns.append(
                    Column(column.name, column_type(column.length), **column.kwargs))
            elif column.type == 'numeric':
                columns.append(
                    Column(column.name, column_type(20, 10), **column.kwargs))
            elif column.type == 'decimal':
                columns.append(
                    Column(column.name, column_type(20, 10), **column.kwargs))
            else:
                columns.append(Column(column.name, column_type, **column.kwargs))

        return columns

    @classmethod
    def insert_values(cls, table: Table, values: list, engine):
        with engine.connect() as conn:
            conn.execute(insert(table).values(values))

    @classmethod
    def insert_values_duplicat_do_nothing(cls, table, values, engine, constraint):
        with engine.connect() as conn:
            insert_stmt = insert(table).values(values)
            conn.execute(insert_stmt.on_conflict_do_nothing(constraint=constraint))

    @classmethod
    def column_to_hump_underline(cls, columns: List[AssetColumn]) -> List[AssetColumn]:
        _columns = copy.deepcopy(columns)
        for column in _columns:
            column.name = to_hump_underline(column.name)
        return _columns
