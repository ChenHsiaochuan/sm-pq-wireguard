#!/usr/bin/env bash
#
# run_proverif.sh -- reproducible driver for the auxiliary agility model.
#
# Runs the positive suite-binding model and the negative regression model,
# capturing raw ProVerif stdout/stderr and an environment fingerprint under
# results/.  Exits 0 only if BOTH models produce their expected verdicts:
#   - positive: all three RESULT lines TRUE
#   - negative: not event(Bad) is false  (i.e. Bad reachable)
#
set -u
cd "$(dirname "$0")"
mkdir -p results

PV="${PROVERIF:-proverif}"

echo "== environment =="
{
  date -Iseconds
  uname -a
  "$PV" 2>&1 | head -1 || true
} > results/agility_environment.txt
cat results/agility_environment.txt

run() {
  local model="$1"
  echo "== running $model =="
  "$PV" "$model" > "results/$model.log" 2> "results/$model.err"
  grep -E "^RESULT" "results/$model.log" || true
}

run agility_suite_model.pv
run agility_suite_regression_bad.pv

# --- verdict gate ---
pos_true=$(grep -cE "^RESULT.* is true\.$" results/agility_suite_model.pv.log || true)
bad_reach=$(grep -cE "^RESULT not event\(Bad\(?\)?\) is false\.$|^RESULT not event\(Bad\) cannot be proved\.$" results/agility_suite_regression_bad.pv.log || true)

echo "positive TRUE results: $pos_true (expect 3)"
echo "negative Bad reachable: $bad_reach (expect >=1)"

if [ "$pos_true" -eq 3 ] && [ "$bad_reach" -ge 1 ]; then
  echo "OVERALL: PASS"
  exit 0
else
  echo "OVERALL: UNEXPECTED VERDICTS"
  exit 1
fi
