#!/bin/bash

# Workspace Health Check Script
# Verifies all workspace services are running correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🏥 Running Workspace Health Checks${NC}"
echo ""

# Check if docker-compose file exists
if [ ! -f "docker-compose.yml" ] && [ ! -f ".devcontainer/docker-compose.yml" ]; then
  echo -e "${RED}❌ No docker-compose.yml found${NC}"
  exit 1
fi

# Determine compose file location
COMPOSE_FILE="docker-compose.yml"
if [ -f ".devcontainer/docker-compose.yml" ]; then
  COMPOSE_FILE=".devcontainer/docker-compose.yml"
fi

# Check Docker is running
echo "🐳 Checking Docker..."
if ! docker info >/dev/null 2>&1; then
  echo -e "${RED}❌ Docker is not running${NC}"
  exit 1
fi
echo -e "${GREEN}✅ Docker is running${NC}"

# Check containers are running
echo ""
echo "📦 Checking containers..."
EXPECTED_SERVICES=$(docker-compose -f "$COMPOSE_FILE" config --services)
RUNNING_SERVICES=$(docker-compose -f "$COMPOSE_FILE" ps --services --filter "status=running")

ALL_RUNNING=true
for service in $EXPECTED_SERVICES; do
  if echo "$RUNNING_SERVICES" | grep -q "^${service}$"; then
    echo -e "${GREEN}✅ $service${NC}"
  else
    echo -e "${RED}❌ $service (not running)${NC}"
    ALL_RUNNING=false
  fi
done

if [ "$ALL_RUNNING" = false ]; then
  echo ""
  echo -e "${YELLOW}Some containers are not running. Run 'docker-compose up -d' to start them.${NC}"
  exit 1
fi

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check PostgreSQL if it exists
if echo "$RUNNING_SERVICES" | grep -q postgres; then
  echo -n "PostgreSQL: "
  if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Healthy${NC}"
  else
    echo -e "${RED}❌ Unhealthy${NC}"
  fi
fi

# Check Redis if it exists
if echo "$RUNNING_SERVICES" | grep -q redis; then
  echo -n "Redis: "
  if docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Healthy${NC}"
  else
    echo -e "${RED}❌ Unhealthy${NC}"
  fi
fi

# Check MongoDB if it exists
if echo "$RUNNING_SERVICES" | grep -q mongo; then
  echo -n "MongoDB: "
  if docker-compose -f "$COMPOSE_FILE" exec -T mongo mongosh --eval "db.runCommand('ping')" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Healthy${NC}"
  else
    echo -e "${RED}❌ Unhealthy${NC}"
  fi
fi

# Check disk usage
echo ""
echo "💾 Checking disk usage..."
DISK_USAGE=$(docker system df -v 2>/dev/null | grep "Local Volumes" | awk '{print $4}')
echo "Docker volumes: $DISK_USAGE"

IMAGES_SIZE=$(docker system df -v 2>/dev/null | grep "Images" | awk '{print $4}')
echo "Docker images: $IMAGES_SIZE"

# Check resource usage
echo ""
echo "📊 Checking resource usage..."
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 10

# Network connectivity
echo ""
echo "🌐 Checking network connectivity..."
if docker-compose -f "$COMPOSE_FILE" exec -T workspace ping -c 1 8.8.8.8 >/dev/null 2>&1; then
  echo -e "${GREEN}✅ Internet connectivity${NC}"
else
  echo -e "${RED}❌ No internet connectivity${NC}"
fi

# Check ports
echo ""
echo "🔌 Checking exposed ports..."
docker-compose -f "$COMPOSE_FILE" ps --format "table {{.Name}}\t{{.Ports}}"

echo ""
echo -e "${GREEN}✅ All health checks completed${NC}"
