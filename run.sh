#!/usr/bin/env sh
ag -l | entr -c bash -c "pytest --exitfirst -v ./$1.py && ./$1.py"
