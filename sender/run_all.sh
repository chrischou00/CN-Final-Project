#!/bin/bash
set -euo pipefail

if [[ "${UID}" -ne 0 ]]; then
  echo "You must be root to run this."
  exit 1
fi

#Run 5 aggregated TCP test
./run.sh -f

sleep 10s

#Run single TCP test
./run.sh
