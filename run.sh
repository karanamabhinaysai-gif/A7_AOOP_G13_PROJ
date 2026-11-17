#!/usr/bin/env bash
set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$BASE_DIR/bin"
mkdir -p "$BIN_DIR"

echo "Compiling Java 17 sources..."
find "$BASE_DIR/src/main/java" -name "*.java" > "$BASE_DIR/sources.txt"
javac -encoding UTF-8 -d "$BIN_DIR" @"$BASE_DIR/sources.txt"
rm "$BASE_DIR/sources.txt"

echo "Running Main Application..."
java -Dfile.encoding=UTF-8 -cp "$BIN_DIR" com.bookmyshow.app.Main
