#!/bin/bash
set -euo pipefail

if [[ "${UID}" != 0 ]]; then
  echo "You must be root to run this."
  exit 1
fi

usage() {
  printf "Usage: %s -t <target> [-p <TCP probe output>] [-n <Number of TCP connections>]\n" "$0"
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

if [[ ! -z "${PROBE_OUTPUT}" ]]; then
  rmmod tcp_probe 2>/dev/null || true
  modprobe tcp_probe full=1 port=5001
  dd if=/proc/1/net/tcpprobe of="${PROBE_OUTPUT}" ibs=128 obs=128 status=none &
  PROBE_PID="$!"
  defer() {
    kill "${PROBE_PID}"
    rmmod tcp_probe
  }
  trap defer EXIT
fi

iperf -t 600 -c "${TARGET}" -P "${NTCP}" > /dev/null

