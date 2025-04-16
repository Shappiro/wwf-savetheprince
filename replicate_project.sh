#!/bin/bash

# replicate_project.sh
# Script to help replicate the WWF-TN-Prince project on another server
# This script handles database export, environment setup, and project configuration

set -e  # Exit on error

# Color codes for prettier output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== WWF-TN-Prince Project Replication Tool ===${NC}"
echo "This script will help you replicate this project on another server"
echo

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}PostgreSQL is not installed. Please install PostgreSQL and PostGIS first.${NC}"
    echo "You can install it with:"
    echo "  sudo apt update"
    echo "  sudo apt install postgresql postgresql-contrib postgis"
    exit 1
fi

# Function to read database credentials
read_db_credentials() {
    # Try to load from existing .env file if present
    if [ -f "src/wwf_prince/settings/local.env" ]; then
        echo -e "${GREEN}Found existing local.env file. Loading credentials...${NC}"
        source <(grep -v '^#' src/wwf_prince/settings/local.env | sed 's/^/export /')
    else
        # Otherwise prompt for credentials
        echo -e "${YELLOW}Please enter your database credentials:${NC}"
        read -p "Database name: " DATABASE_NAME
        read -p "Database user: " DATABASE_USER
        read -p "Database password: " -s DATABASE_PW
        echo
        read -p "Database host (default: localhost): " DATABASE_HOST
        DATABASE_HOST=${DATABASE_HOST:-localhost}
        read -p "Database port (default: 5432): " DATABASE_PORT
        DATABASE_PORT=${DATABASE_PORT:-5432}
    fi
}

# Backup the database
backup_database() {
    echo -e "${BLUE}Backing up the database...${NC}"
    BACKUP_DIR="backups"
    BACKUP_FILE="$BACKUP_DIR/$(date +%Y%m%d)_$DATABASE_NAME.dump"
    
    mkdir -p "$BACKUP_DIR"
    
    # Create a custom format dump (most versatile for restoration)
    PGPASSWORD=$DATABASE_PW pg_dump \
        -h $DATABASE_HOST \
        -p $DATABASE_PORT \
        -U $DATABASE_USER \
        -F c \
        -b \
        -v \
        -f "$BACKUP_FILE" \
        $DATABASE_NAME
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Database backup created: $BACKUP_FILE${NC}"
    else
        echo -e "${RED}Database backup failed!${NC}"
        exit 1
    fi
}

# Create environment variables file for the new server
create_env_file() {
    echo -e "${BLUE}Creating environment file template for new server...${NC}"
    
    ENV_TEMPLATE="env_template.env"
    cat > "$ENV_TEMPLATE" << EOF
# Database settings
DATABASE_NAME=$DATABASE_NAME
DATABASE_USER=$DATABASE_USER
DATABASE_PW=$DATABASE_PW
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email settings
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# Security
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

# Captcha
CAPTCHA_PUBLIC_KEY=your_captcha_public_key
CAPTCHA_PRIVATE_KEY=your_captcha_private_key
EOF
    
    echo -e "${GREEN}Environment template created: $ENV_TEMPLATE${NC}"
    echo "Update this with your new server's details and place it at src/wwf_prince/settings/local.env"
}

# Create instructions for setup on the new server
create_setup_instructions() {
    echo -e "${BLUE}Creating setup instructions for the new server...${NC}"
    
    INSTRUCTIONS="SETUP_INSTRUCTIONS.md"
    cat > "$INSTRUCTIONS" << 'EOF'
# WWF-TN-Prince Project Setup Instructions

Follow these instructions to set up the project on a new server.

## Prerequisites

1. Install required system packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git postgresql postgresql-contrib postgis
   ```

2. Install GDAL development libraries (required for GeoDjango):
   ```bash
   sudo apt install binutils libproj-dev gdal-bin libgdal-dev
   ```

## Database Setup

1. Create a new PostgreSQL database and user:
   ```bash
   sudo -u postgres psql
   ```

   In the PostgreSQL console:
   ```sql
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   CREATE DATABASE your_db_name;
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   \c your_db_name
   CREATE EXTENSION postgis;
   CREATE EXTENSION postgis_topology;
   \q
   ```

2. Restore the database from backup:
   ```bash
   sudo -u postgres pg_restore -d your_db_name /path/to/database_backup.dump
   ```

## Project Setup

1. Clone the repository:
   ```bash
   git clone <repository_url> /var/www/wwf-tn-prince
   cd /var/www/wwf-tn-prince
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp env_template.env src/wwf_prince/settings/local.env
   # Edit local.env with the correct settings
   nano src/wwf_prince/settings/local.env
   ```

5. Collect static files:
   ```bash
   cd src
   python manage.py collectstatic --noinput
   ```

6. Apply any pending migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (if not already in the restored database):
   ```bash
   python manage.py createsuperuser
   ```

## Web Server Setup

For production deployment, you'll need to configure a web server like Nginx with Gunicorn:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create a systemd service for Gunicorn:
   ```bash
   sudo nano /etc/systemd/system/wwf-tn-prince.service
   ```

   Add the following content (adjust paths as needed):
   ```
   [Unit]
   Description=WWF-TN-Prince Gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/wwf-tn-prince/src
   ExecStart=/var/www/wwf-tn-prince/env/bin/gunicorn \
     --access-logfile - \
     --workers 3 \
     --bind unix:/var/www/wwf-tn-prince/gunicorn.sock \
     wwf_prince.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

3. Start and enable the service:
   ```bash
   sudo systemctl start wwf-tn-prince
   sudo systemctl enable wwf-tn-prince
   ```

4. Install and configure Nginx:
   ```bash
   sudo apt install nginx
   sudo nano /etc/nginx/sites-available/wwf-tn-prince
   ```

   Add the following configuration (adjust as needed):
   ```
   server {
       listen 80;
       server_name your_domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /var/www/wwf-tn-prince;
       }

       location /media/ {
           root /var/www/wwf-tn-prince;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/wwf-tn-prince/gunicorn.sock;
       }
   }
   ```

5. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/wwf-tn-prince /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## Security Considerations

1. Set up SSL/TLS with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```

2. Configure firewall:
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw allow OpenSSH
   sudo ufw enable
   ```

3. Ensure proper file permissions:
   ```bash
   sudo chown -R www-data:www-data /var/www/wwf-tn-prince/media_cdn
   sudo chown -R www-data:www-data /var/www/wwf-tn-prince/static_cdn
   ```
EOF
    
    echo -e "${GREEN}Setup instructions created: $INSTRUCTIONS${NC}"
}

# Create a requirements.txt file if not exists
create_requirements_file() {
    echo -e "${BLUE}Creating/updating requirements.txt file...${NC}"
    
    if [ -f "src/requirements.txt" ]; then
        echo -e "${GREEN}Using existing requirements.txt file in src directory${NC}"
    else
        if [ -f "Pipfile" ]; then
            echo -e "${YELLOW}Found Pipfile. Converting to requirements.txt...${NC}"
            if command -v pipenv &> /dev/null; then
                pipenv lock -r > requirements.txt
            else
                echo -e "${RED}Pipenv not installed. Please install it or create requirements.txt manually.${NC}"
                echo "You can install pipenv with: pip install pipenv"
            fi
        else
            echo -e "${YELLOW}Creating a basic requirements.txt file based on project structure...${NC}"
            cat > "requirements.txt" << EOF
# Core libraries
Django>=3.2,<4.0
psycopg2-binary>=2.9.1
python-decouple>=3.4
django-environ>=0.4.5

# Authentication and permissions
django-authtools>=2.0.0
django-crispy-forms>=1.12.0

# GeoDjango dependencies
django-leaflet>=0.28.0
django-geojson>=3.2.0

# Admin interface
django-admin-interface>=0.16.3
django-related-admin>=0.8.0
django-ajax-selects>=2.1.0
django-ordered-model>=3.5
django-colorfield>=0.4.2
django-filebrowser>=3.14.0
django-tinymce>=3.3.0

# Images and media
sorl-thumbnail>=12.7.0
django-imagekit>=4.0.2

# API and data
djangorestframework>=3.12.4
djangorestframework-gis>=0.17
django-filter>=2.4.0
djangorestframework-datatables>=0.6.0
django-tables2>=2.3.4

# Utilities
django-extensions>=3.1.3
django-phonenumber-field>=5.2.0
django-cookielaw>=2.0.3
django-localflavor>=3.1
django-queryable-properties>=1.7.0
django-controlcenter>=0.3.2
django-captcha>=0.1.0

# Additional dependencies based on project structure
sentry-sdk>=1.3.1
EOF
        fi
    fi
    
    echo -e "${GREEN}Requirements file prepared${NC}"
}

main() {
    read_db_credentials
    backup_database
    create_env_file
    create_requirements_file
    create_setup_instructions
    
    echo
    echo -e "${GREEN}All tasks completed successfully!${NC}"
    echo
    echo -e "To replicate this project on another server:"
    echo "1. Copy the entire project directory (using git clone or scp)"
    echo "2. Copy the database backup: $BACKUP_FILE"
    echo "3. Copy the environment template: $ENV_TEMPLATE"
    echo "4. Follow the instructions in: SETUP_INSTRUCTIONS.md"
    echo
}

main