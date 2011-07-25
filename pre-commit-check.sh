#!/bin/bash

echo 'Running tests'
bin/test -s collective.table

echo '====== Running PyFlakes ======'
bin/pyflakes collective/table
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 collective/table
bin/pep8 setup.py
