# Automate Salesforce Sandbox/Scratch Org Data Seeding with Snowfakery and SFDMU

## Description

Integrating Snowfakery with SFDMU offers a powerful solution for Salesforce scratch org and sandbox data seeding. By leveraging Snowfakery's ability to generate complex, realistic test data and SFDMU's robust data migration capabilities, you can streamline your development and testing workflows.

## Installation and data seeding in Sandbox

1. Install Snowfakery and SFDMU:
   [Snowfakery installation Documentation](https://snowfakery.readthedocs.io/en/latest/#installation-for-non-salesforce-users)
   [SFDMU installation Documentation](https://help.sfdmu.com/installation)
```bash
   $ pip3 install pipx
   $ pipx install snowfakery
   $ sf plugins install sfdmu
   ```
   

2. Clone the repository:

```bash
git clone https://github.com/junliu724515/snowfakery_with_sfdmu.git

```

3. Navigate to the project directory:

```bash
cd snowfakery_with_sfdmu
```

4. Generating Test Data with Snowfakery

```bash
snowfakery snowfakery/Account_Opportunity_Contact.recipe.yml --output-format csv --output-folder test-data/
```

5. Convert Data and Generate export.json Metadata File for SFDMU

```bash
python3 scripts/generate_export_json.py test-data
```

6. Run SFDMU Data Load

```bash
#Replace `{{your target org}}` with your sandbox org alias
sf sfdmu run --sourceusername csvfile  --targetusername {{your target org}} --path test-data
```

## Automate a scratch org creation with the test data uploaded using Snowfakery and SFDMU

1. Replace {{your DevHub}} with your DevHub alias in the `scripts/spin-up-scratch-org.sh` file.
2. Run the script to create a scratch org and upload the test data.
```bash
./scripts/spin-up-scratch-org.sh
```
3. Or run window batch file if you use windows.
```bash
./scripts/spin-up-scratch-org.bat
```
    