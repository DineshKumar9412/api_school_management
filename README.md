# api_school_management
Implement a School Management System API

# step install 
install basic software 
docker
******
sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
docker --version

sudo apt update
sudo apt install -y docker-compose-plugin
docker compose version

install for python 3.10 for testing 
************************************
sudo apt update

sudo apt install software-properties-common -y

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.10 python3.10-venv python3.10-dev -y

python3.10 --version

create a ENV

Create a virtual environment named 'school_env' using Python 3.10
python3.10 -m venv school_env

source school_env/bin/activate

Upgrade pip to the latest version
pip install --upgrade pip

Install all dependencies listed in requirements.txt
pip install -r requirements.txt

Run the FastAPI app using Uvicorn on all network interfaces (0.0.0.0) at port 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000


git clone https://github.com/DineshKumar9412/api_school_management.git

cd api_school_management/

vi .env

# DATABASE
DB_USER="root"
DB_PASSWORD="Root@123"
DB_HOST="localhost"
DB_NAME="sampledb"
DB_PORT="3306"

# REDIS 
REDIS_HOST="127.0.0.1"
REDIS_PORT="6379"
REDIS_PASSWORD="Redis@123"

# ENCRYPTION KEY
KEY="MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY="
IV="YWJjZGVmOTg3NjU0MzIxMA=="

# SONAR TOKEN 
SONAR_TOKEN="squ_f432f3d48f716e518958d90e29c27bb64bbbf7eb"

cd /api_school_management/infra/preprod

cd infra/preprod
sudo docker compose down -v
sudo docker compose build --no-cache
sudo docker compose up -d

sudo docker logs school-app-preprod --tail=20


working 


services:
  loki:
    image: grafana/loki:3.0.0
    container_name: loki-preprod
    command: -config.file=/etc/loki/loki.yaml
    ports:
      - "3100:3100"
    volumes:
      - ./loki.yaml:/etc/loki/loki.yaml
      - loki-preprod-data:/loki
    restart: unless-stopped

  grafana:
    image: grafana/grafana:10.2.3
    container_name: grafana-preprod
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-preprod-data:/var/lib/grafana
    depends_on:
      - loki
    restart: unless-stopped

  app:
    container_name: school-app-preprod
    build:
      context: ../../
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - loki
    restart: unless-stopped

volumes:
  loki-preprod-data:
  grafana-preprod-data:









auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

ingester:
  chunk_idle_period: 3m
  chunk_retain_period: 1m

compactor:
  working_directory: /loki/compactor
  retention_enabled: true
  delete_request_store: filesystem

limits_config:
  retention_period: 168h        # ✅ 7 days (PRE-PROD)
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_streams_per_user: 0

table_manager:
  retention_deletes_enabled: true
  retention_period: 168h

