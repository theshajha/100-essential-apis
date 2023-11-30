#!/bin/bash

# Set your desired directory, Git repository URL, username, and password
DIRECTORY=""
GIT_REPO_URL=""
GIT_USERNAME=""
GIT_PASSWORD=""

# Check current directory and change if necessary
if [ "$(pwd)" != "$DIRECTORY" ]; then
  cd "$DIRECTORY"
fi

# Install necessary packages
if ! command -v docker &> /dev/null; then
  echo "Docker not found. Installing Docker..."
  sudo apt-get update
  sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io
fi

if ! command -v docker-compose &> /dev/null; then
  echo "Docker Compose not found. Installing Docker Compose..."
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

# Clone the repository
if ! command -v git &> /dev/null; then
echo "Git not found. Installing Git..."
sudo apt-get install -y git
fi

cd "$DIRECTORY"
echo "Pulling new changes from the repository..."
GIT_URL_WITH_CREDENTIALS="${https://$GIT_USERNAME:$GIT_PASSWORD@GIT_REPO_URL/}"
sudo git pull "$GIT_URL_WITH_CREDENTIALS"

# Build and run the Docker containers
echo "Building and running Docker containers..."
docker compose up --build -d

echo "Done."
