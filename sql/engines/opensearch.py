# -*- coding: UTF-8 -*-
import os
import re, time
import logging

import simplejson as json
from sql.engines.elastic_search_engine_base import ElasticsearchEngineBase

from . import EngineBase
from .models import ResultSet, ReviewSet, ReviewResult
from common.config import SysConfig
from opensearchpy import OpenSearch


logger = logging.getLogger("default")


class OpenSearchEngine(ElasticsearchEngineBase):
    """OpenSearch 引擎实现"""

    def __init__(self, instance=None):
        super().__init__(instance=instance)

    name: str = "OpenSearch"
    info: str = "OpenSearch 引擎"

    def get_connection(self, db_name=None):
        if self.conn:
            return self.conn
        if self.instance:
            scheme = "https" if self.is_ssl else "http"
            hosts = [
                {
                    "host": self.host,
                    "port": self.port,
                    "scheme": scheme,
                    "use_ssl": self.is_ssl,
                }
            ]
            http_auth = (
                (self.user, self.password) if self.user and self.password else None
            )
            self.db_name = (self.db_name or "") + "*"

            try:
                # 创建 OpenSearch 连接
                self.conn = OpenSearch(
                    hosts=hosts,
                    http_auth=http_auth,
                    verify_certs=True,  # 开启证书验证
                )
            except Exception as e:
                raise Exception(f"OpenSearch 连接建立失败: {str(e)}")
        if not self.conn:
            raise Exception("OpenSearch 连接无法建立。")
        return self.conn
