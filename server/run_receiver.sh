#!/bin/bash
set -euo pipefail
sudo sysctl -q -w net.ipv4.tcp_sack=0
sudo sysctl -q -w net.ipv4.tcp_dsack=0
sudo sysctl -q -w net.ipv4.tcp_fack=0
iperf3 -s >/dev/null &
