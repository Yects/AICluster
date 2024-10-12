
# Create standalone executables using PyInstaller

# Ensure we are in the correct directory
cd "$(dirname "$0")"

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip setuptools wheel pyinstaller
pip install .

# Function to create standalone executable for a given platform
create_executable() {
    local platform=$1

    echo "Creating standalone executable for $platform..."

    if [ "$platform" == "linux" ]; then
        EXO_NAME=exo-linux pyinstaller exo.spec
    elif [ "$platform" == "macos" ]; then
        # Install Homebrew if not already installed (for macOS)
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi

        EXO_NAME=exo-macos pyinstaller exo.spec
    elif [ "$platform" == "windows" ]; then
        # Install Wine if not already installed (for cross-compiling Windows executables on Linux)
        if ! command -v wine &> /dev/null; then
            echo "Wine not found. Installing Wine..."
            sudo apt-get update && sudo apt-get install -y wine64
        fi

        EXO_NAME=exo-windows pyinstaller exo.spec
    else
        echo "Unsupported platform: $platform"
        exit 1
    fi

    echo "Standalone executable for $platform created successfully."
}

# Create executables for all target platforms (Linux, macOS, Windows)
create_executable linux
create_executable macos
create_executable windows
