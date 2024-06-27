#!/bin/bash

# Step 1: Create a new scratch org
echo "Creating a new scratch org..."
sf org create scratch --definition-file config/project-scratch-def.json --alias SnowfakeryDemo --target-dev-hub JM_PBO

## Step 2: deploy code
sf project deploy start  --target-org SnowfakeryDemo

# Step 3: Generate fake data using Snowfakery
echo "Generating fake data..."
snowfakery snowfakery/Account_Contact_Case_Opportunity_Role_Reservation.yml --output-format csv --output-folder test-data/

# Step 4: Use the Python script to prepare the data for upload
echo "Preparing data and Generating export.json for upload..."
python3 scripts/generate_export_json.py test-data

# Step 5: Upload the data to the scratch org using SFDMU
echo "Uploading data to the scratch org..."
sf sfdmu run --sourceusername csvfile  --targetusername SnowfakeryDemo --path test-data