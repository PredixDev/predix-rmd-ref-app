#!/bin/bash
set -e


function local_read_args() {
  while (( "$#" )); do
  opt="$1"
  case $opt in
    -h|-\?|--\?--help)
      PRINT_USAGE=1
      QUICKSTART_ARGS="$SCRIPT $1"
      break
    ;;
    -b|--branch)
      BRANCH="$2"
      QUICKSTART_ARGS+=" $1 $2"
      shift
    ;;
    -o|--override)
      QUICKSTART_ARGS=" $SCRIPT"
    ;;
    --skip-setup)
      SKIP_SETUP=true
    ;;
    --skip-pull)
      SKIP_PULL=true
    ;;
    *)
      QUICKSTART_ARGS+=" $1"
      #echo $1
    ;;
  esac
  shift
  done

  if [[ -z $BRANCH ]]; then
    echo "Usage: $0 -b/--branch <branch> [--skip-setup]"
    exit 1
  fi
}

BRANCH="master"
PRINT_USAGE=0
SKIP_SETUP=false
SKIP_PULL=false
ASSET_MODEL="-amrmd predix-webapp-starter/server/sample-data/predix-asset/asset-model-metadata.json predix-webapp-starter/server/sample-data/predix-asset/asset-model.json"
SCRIPT="-script build-basic-app.sh -script-readargs build-basic-app-readargs.sh"
QUICKSTART_ARGS="-ba -uaa -asset -ts -wss -dx -sim -rmd $ASSET_MODEL -psrmd $SCRIPT"
IZON_SH="https://raw.githubusercontent.com/PredixDev/izon/1.0.0/izon.sh"
VERSION_JSON="version.json"
PREDIX_SCRIPTS=predix-scripts
REPO_NAME=predix-rmd-ref-app
VERSION_JSON="version.json"
APP_NAME="RMD Asset Monitoring Reference App"
SCRIPT_NAME=quickstart-rmd-ref-app.sh
TOOLS="Cloud Foundry CLI, Git, Java JDK, Maven, Node.js"
TOOLS_SWITCHES="--cf --git --jdk --maven --nodejs"

local_read_args $@
VERSION_JSON_URL=https://raw.githubusercontent.com/PredixDev/predix-rmd-ref-app/$BRANCH/version.json

function check_internet() {
  set +e
  echo ""
  echo "Checking internet connection..."
  curl "http://google.com" > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Unable to connect to internet, make sure you are connected to a network and check your proxy settings if behind a corporate proxy"
    echo "If you are behind a corporate proxy, set the 'http_proxy' and 'https_proxy' environment variables."
    exit 1
  fi
  echo "OK"
  echo ""
  set -e
}

function init() {
  currentDir=$(pwd)
  if [[ $currentDir == *"scripts" ]]; then
    echo 'Please launch the script from the root dir of the project'
    exit 1
  fi

  check_internet
  #if needed, get the version.json that resolves dependent repos from another github repo
  if [ ! -f "$VERSION_JSON" ]; then
    if [[ $currentDir == *"$REPO_NAME" ]]; then
      if [[ ! -f manifest.yml ]]; then
        echo 'We noticed you are in a directory named $REPO_NAME but the usual contents are not here, please rename the dir or do a git clone of the whole repo.  If you rename the dir, the script will get the repo.'
        exit 1
      fi
    fi
    echo $VERSION_JSON_URL
    curl -s -O $VERSION_JSON_URL
  fi

  #get the script that reads version.json
  eval "$(curl -s -L $IZON_SH)"
  #get the url and branch of the requested repo from the version.json
  #__readDependency "local-setup" LOCAL_SETUP_URL LOCAL_SETUP_BRANCH
  #get the predix-scripts url and branch from the version.json
  if [ ! -d "../predix-rmd-ref-app" ]; then
    __readDependency "predix-rmd-ref-app" PREDIX_REFAPP_URL PREDIX_REFAPP_BRANCH
    git clone --depth 1 --branch $PREDIX_REFAPP_BRANCH $PREDIX_REFAPP_URL
    cd predix-rmd-ref-app
  fi

  echo "Pulling Submodules"
  if ! $SKIP_PULL; then
    ./scripts/pullSubModules.sh
  fi
  source $PREDIX_SCRIPTS/bash/scripts/local-setup-funcs.sh
}


if [[ $PRINT_USAGE == 1 ]]; then
  init
  __print_out_standard_usage
else
  if $SKIP_SETUP; then
    init
  else
    init
    __standard_mac_initialization
  fi
fi


echo "quickstart_args=$QUICKSTART_ARGS"
source $PREDIX_SCRIPTS/bash/quickstart.sh $QUICKSTART_ARGS

__append_new_line_log "Successfully completed $APP_NAME installation!" "$quickstartLogDir"
