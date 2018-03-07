#! /usr/bin/env bash
set -x
git submodule init
git submodule update --rebase --remote
