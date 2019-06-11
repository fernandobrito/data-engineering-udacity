#!/bin/bash

{ python3 create_tables.py; python3 etl.py; } 2>&1 | tee -a "logs/$(date +"%Y-%m-%d-%H:%M:%S").txt"