# Docker Quick Start

## Prerequisites
- Docker installed ([Download](https://www.docker.com/get-started))

## Start the API

```bash
# Clone the repository
git clone <repository-url>
cd FinalProject

# Start the API
docker-compose up --build
```

The API will be available at **http://localhost:8000**

## Test the API

1. Open http://localhost:8000/docs in your browser
2. Try the `/sample-data` endpoint to get sample customer data
3. Use that data with `/predict/v1_lr`, `/predict/v2_rf`, or `/predict/v3_gb`

## Common Commands

```bash
# Start in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

That's it! 🚀
