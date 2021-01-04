#!/bin/bash
set -euo pipefail

if [[ "${UID}" != 0 ]]; then
  echo "You must be root to run this."
  exit 1
fi

usage() {
  printf "Usage: %s -t <target> [-p <output file>] [-n <Number of TCP connections>]\n" "$0"
  exit 1
}

PROBE_OUTPUT=
TARGET=
NTCP="1"
while getopts :p:t:n: OPT; do
  case "${OPT}" in
    p)
      PROBE_OUTPUT="${OPTARG}"
      ;;
    t)
      TARGET="${OPTARG}"
      ;;
    n)
      NTCP="${OPTARG}"
      ;;
    \?|:)
      usage
      ;;
  esac
done

if [[ -z "${TARGET}" ]]; then
  usage
fi

if [ "$NTCP" = "5" ]; then
    for count in $(seq 1 1 5); do
        echo "Aggregated Connection Test ${count}"
        iperf3 -t 1000 -c "${TARGET}" -P "${NTCP}" -i "0" | tee -a "${PROBE_OUTPUT}"
        sleep 10s
    done
fi

if [ "$NTCP" = "1" ]; then
    for count in $(seq 1 1 3); do
        echo "Single Connection Test ${count}"
        iperf3 -t 1000 -c "${TARGET}" -i "0" | tee -a "${PROBE_OUTPUT}"
        sleep 10s
    done
fi
