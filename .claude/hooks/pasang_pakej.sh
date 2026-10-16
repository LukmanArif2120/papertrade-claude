#!/usr/bin/env bash
# SessionStart: pasang pakej Python (requirements.txt) dalam sesi awan, termasuk rutin berjadual.
# Tidak sekali-kali menggagalkan sesi; di luar sesi awan tiada apa-apa dibuat.
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" 2>/dev/null || exit 0
python3 -c "import pandas, numpy, exchange_calendars" 2>/dev/null && exit 0
python3 -m pip install -q -r requirements.txt >/dev/null 2>&1 || true
exit 0
