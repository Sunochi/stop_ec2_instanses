#!/bin/bash

LAMBDA_DIR="$(cd "$(dirname "${0}" )"; pwd)"
SCRIPT_DIR="${LAMBDA_DIR}/src"
WORKSPACE="${LAMBDA_DIR}/workspace"
LAMBDA_FUNCTION="${SCRIPT_DIR}/lambda_function.py"
INIT_FILE="${SCRIPT_DIR}/__init__.py"

if [ -d "${WORKSPACE}" ]; then
    rm -rf "${WORKSPACE}"
fi

mkdir -p "${WORKSPACE}"

cp "${LAMBDA_FUNCTION}" "${WORKSPACE}"
cp "${INIT_FILE}" "${WORKSPACE}"

pip install -r "${SCRIPT_DIR}/requirements.txt" -t "${WORKSPACE}"
