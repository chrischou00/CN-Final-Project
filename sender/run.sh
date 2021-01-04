#!/bin/bash
set -euo pipefail

if [[ "${UID}" -ne 0 ]]; then
  echo "You must be root to run this."
  exit 1
fi

# "full" mode runs 5 aggregated TCP.
full=false
ntcp=1
while getopts 'abfv' flag; do
  case "${flag}" in
    f) full=true ;;
    *) error "Use either 'sudo ./run.sh' or 'sudo ./run.sh -f'." ;;
  esac
done

max_burst=0.15
max_period=5.0
if [ "$full" = true ]; then
  max_burst=0.10
  max_period=5.0
  ntcp=5
fi

START_TIME=`date +%Y%m%d-%H%M%S`
HOSTNAME=`hostname`

for burst in $(seq ${max_burst} 0.05 ${max_burst}); do
  for period in $(seq 0.5 0.05 2.0); do
    killall -9 python dd nc tshark dumpcap iperf3 || true
    echo ""
    echo "Attack parameters: burst=${burst}, period=${period}"

    python dos.py --rto=1000 --period "${period}" --burst "${burst}" \
                  --suffix "${HOSTNAME}-${START_TIME}" --nc "${ntcp}"
    killall -9 python dd nc tshark dumpcap iperf3 || true

    echo ""
    echo "Done."

    sleep 5s
  done

  for period in $(seq 2.1 0.1 ${max_period}); do
    killall -9 python dd nc tshark dumpcap iperf3 || true
    echo ""
    echo "Attack parameters: burst=${burst}, period=${period}"

    python dos.py --rto=1000 --period "${period}" --burst "${burst}" \
                  --suffix "${HOSTNAME}-${START_TIME}" --nc "${ntcp}"
    killall -9 python dd nc tshark dumpcap iperf3 || true

    echo ""
    echo "Done."

    sleep 5s
  done

done

su $SUDO_USER -c ./plot_bw.py

