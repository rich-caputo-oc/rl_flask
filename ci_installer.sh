#!/bin/bash -l
# usage example: /bin/bash ci_installer.sh your-github-token 1.x oncorps-python-library-ci.yml
mkdir -p .github/workflows && curl -s -O https://"${1}"@raw.githubusercontent.com/OnCorps/.github/"${2}"/workflow-templates/"${3}" &&  mv "${3}" .github/workflows/continuous-integration-workflow.yml
