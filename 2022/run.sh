#!/usr/bin/env sh
export fprefix=$1
shift
ag -l | \
entr -c \
bash -c "~/.venvs/aoc/bin/python3 -m pytest --tb=native -vv ./$fprefix.py $@ && ./$fprefix.py"
