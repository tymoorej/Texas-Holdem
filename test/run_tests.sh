#!/usr/bin/env bash

for f in `find . -name '*tests*.py'`; do
    echo ---- Running ${f} ----
    python3 ${f}
done
