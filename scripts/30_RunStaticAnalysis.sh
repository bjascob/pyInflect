#!/bin/sh

# Static analysis checker'

# Disable the following errors
# see https://docs.pylint.org/en/1.6.0/features.html
DISABLES="--disable=C0326,R0205,R1705,R1710,R0911,R0912,R0903,C0103,C0111"

# Run the command
pylint $DISABLES ../pyinflect
