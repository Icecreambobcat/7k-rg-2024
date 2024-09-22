#!bin/zsh

ask_for_confirmation() {
  while true; do
    read -p "$1 (y/n/a for abort): " yn
    case $yn in
      [Yy]*) return 0 ;;  # Yes
      [Nn]*) return 1 ;;  # No
      [Aa]*) echo "Operation aborted."; exit 1 ;;  # Abort
      *) echo "Please answer yes, no, or abort." ;;
    esac
  done
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
REPO_DIR="$SCRIPT_DIR/../.."

cd "$REPO_DIR"

# Check if the .git directory exists
if [ ! -d ".git" ]; then
  echo ".git folder does not exist."
  if ask_for_confirmation "Do you want to remove and re-clone the repository?"; then
    echo "Removing $REPO_DIR and cloning the repository..."
    rm -rf "$REPO_DIR" && git clone https://github.com/Icecreambobcat/4k-rg-2024 "$REPO_DIR"
  else
    echo "Operation canceled."
  fi
  exit 1
fi

git fetch

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ "$LOCAL" = "$REMOTE" ]; then
  # If up2date
  if ask_for_confirmation "Up to date. Launch?"; then
    python3 src/init/main.py
  else
    echo "Cancelled."
  fi

elif [ "$LOCAL" = "$BASE" ]; then
  #if behind
  if ask_for_confirmation "Update available. Update?"; then
    git pull
    echo "Updated."
  else
    echo "Deferred."
  fi
  if ask_for_confirmation "Launch?"; then
    python3 src/init/main.py
  else
    echo "Cancelled."
  fi

else
  # unexpected
  if ask_for_confirmation "Unexpected filestructure detected. Attempt to reinstall?"; then
    rm -rf $REPO_DIR && git clone https://github.com/Icecreambobcat/4k-rg-2024 "$REPO_DIR"
  else
    echo "It is strongly advised to reinstall given the unknown state of the filestructure of the project. However, proceed at your own risk."
  fi
