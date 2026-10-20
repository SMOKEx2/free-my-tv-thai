#!/usr/bin/env bash
# Source build for hosts with Python 3, JDK 17 and Android build-tools 34 already available.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 tools/build.py --sdk-root "${ANDROID_HOME:?Set ANDROID_HOME}" --java-home "${JAVA_HOME:?Set JAVA_HOME}" "$@"
