#!/usr/bin/env sh
ag -l | entr -rc bash -c "pytest --exitfirst -v ./$1.py && ./$1.py"
