#!/usr/bin/env bash
set -Eeuo pipefail
prefix="${1:-card}"
slug="${2:-item}"
date '+%Y%m%d-%H%M%S' | awk -v p="$prefix" -v s="$slug" '{print p "__" $0 "__" s}'
