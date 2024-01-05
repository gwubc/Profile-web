#!/bin/bash
docker compose -f /home/ubuntu/deploy/compose.yaml  stop ;
docker compose -f /home/ubuntu/deploy/compose.yaml  create ;
docker compose -f /home/ubuntu/deploy/compose.yaml  start ;
