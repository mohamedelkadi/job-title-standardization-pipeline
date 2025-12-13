#!/bin/bash

# Database setup script for LinkedIn member data
# This script creates the database, loads the schema, and imports all CSV data

set -e  # Exit on error

# Default values
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-$(whoami)}"
DB_NAME="${DB_NAME:-linkedin_members}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== LinkedIn Member Data Database Setup ===${NC}"
echo ""
echo "Configuration:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  User: $DB_USER"
echo "  Database: $DB_NAME"
echo ""

# Check if PostgreSQL is accessible
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
    echo -e "${RED}Error: PostgreSQL server is not accessible at $DB_HOST:$DB_PORT${NC}"
    echo "Please ensure PostgreSQL is running and accessible."
    exit 1
fi

# Get password if needed (for non-local connections)
if [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
    echo -e "${YELLOW}Note: You may be prompted for a database password${NC}"
    export PGPASSWORD="${PGPASSWORD:-}"
fi

# Step 1: Create database if it doesn't exist
echo -e "${GREEN}[1/3] Creating database (if it doesn't exist)...${NC}"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME"
echo -e "${GREEN}✓ Database ready${NC}"
echo ""

# Step 2: Load database schema
echo -e "${GREEN}[2/3] Loading database schema...${NC}"
DATA_DIR="$(cd "$(dirname "$0")/li_member_csv_202403" && pwd)"
SCHEMA_FILE="$DATA_DIR/db_structure_postgresql.sql"

if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}Error: Schema file not found at $SCHEMA_FILE${NC}"
    exit 1
fi

psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$SCHEMA_FILE"
echo -e "${GREEN}✓ Schema loaded${NC}"
echo ""

# Step 3: Import CSV data
echo -e "${GREEN}[3/3] Importing CSV data (this may take a while)...${NC}"
echo -e "${YELLOW}This step will decompress CSV files and import them into the database.${NC}"
echo ""

cd "$DATA_DIR"
bash import_postgresql.sh "$DB_HOST" "$DB_PORT" "$DB_USER" "$DB_NAME"

echo ""
echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo "Database connection string:"
echo "  postgresql://$DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
echo ""
echo "You can now connect to the database using:"
echo "  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
echo ""

