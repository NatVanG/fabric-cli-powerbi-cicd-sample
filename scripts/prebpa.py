import os
import time
import argparse
import glob
from utils import *

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--spn-auth", action="store_true", default=True)
parser.add_argument("--workspace", default="SalesSense")
parser.add_argument("--admin-upns", default=os.getenv("FABRIC_ADMIN_UPNS"))
parser.add_argument(
    "--capacity", default=os.getenv("FABRIC_CAPACITY")
)

args = parser.parse_args()

spn_auth = args.spn_auth
capacity_name = args.capacity
workspace_name = args.workspace
admin_upns = args.admin_upns

if admin_upns:
    admin_upns = [upn.strip() for upn in admin_upns.split(",")]

# Authenticate
if spn_auth:
    fab_authenticate_spn()

# Get tenant_settings
tenant_settings = None

for attempt in range(3):

    tenant_settings = run_fab_command(
        f"api admin/tenantsettings",
        capture_output=True,
    )

    if tenant_settings != None and tenant_settings != "":
        break

    print("Waiting for tenant settings...")

    time.sleep(30)

if tenant_settings == None or tenant_settings == "" or tenant_settings == "None":
    raise Exception(f"Cannot resolve tenant settings")

# save tenant settings

# Define the directory and file path
directory = "targetenvironment"
file_path = os.path.join(directory, "tenant-settings.json")

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Write the string to the file
with open(file_path, "w") as file:
    file.write(tenant_settings)


# Log out in case of auth with SPN

if spn_auth:
    run_fab_command("auth logout")
