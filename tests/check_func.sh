#!/usr/bin/env bash


for fname in ../src/brew_file/*.py;do
  name=$(basename "$fname")
  if [ "$name" = "utils.py" ];then
    continue
  fi
  test_file=test_$name
  funcs=$(grep '^    def' "$fname"|awk '{print $2}'|cut -d "(" -f1|grep -v "^__")
  for f in $funcs;do
    if ! grep -q "def test_$f(" "$test_file";then
      echo "$f not in $test_file"
    fi
  done
done
