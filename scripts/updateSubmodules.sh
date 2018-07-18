#!/bin/bash
set -e

GITHUB_REPO="$1"
GITHUB_REPO_BRANCH="$2"
REPO_NAME=$(echo $GITHUB_REPO | awk -F"/" '{print $NF}' | awk -F"." '{print $1}');

echo "GITHUB_REPO $GITHUB_REPO"
echo "REPO_NAME $REPO_NAME"
rm -rf $REPO_NAME
git clone $GITHUB_REPO -b $GITHUB_REPO_BRANCH --recursive
cd $REPO_NAME
git submodule foreach git pull origin develop
git commit -a -m "updating submodules"
git push
