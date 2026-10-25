#!/bin/sh
# Point the global core.hooksPath at this directory.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
current=$(git config --global --get core.hooksPath || true)
if [ -n "$current" ] && [ "$current" != "$here" ]; then
	echo "core.hooksPath is already set to $current; unset it first" >&2
	exit 1
fi
git config --global core.hooksPath "$here"
echo "core.hooksPath -> $here"
