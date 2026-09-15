#!/bin/sh
# Print the liveness.js source so it can be pasted into javascript_tool.
#   sh .claude/skills/rewrite/liveness.sh
cat "$(dirname "$0")/liveness.js"
