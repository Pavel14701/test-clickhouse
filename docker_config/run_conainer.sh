#!/bin/bash
# -*- coding: utf-8 -*-

docker run -d \
  -p 8123:8123 \
  -p 9000:9000 \
  -p 9009:9009 \
  --name my-clickhouse-container \
  my-clickhouse-image