import os
import requests
import zipfile
import subprocess
import tempfile
import shutil
import time
import argparse
import glob
from utils import *

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--spn-auth", action="store_true", default=True)
parser.add_argument("--admin-upns", default=os.getenv("FABRIC_ADMIN_UPNS"))
parser.add_argument(
    "--capacity", default=os.getenv("FABRIC_CAPACITY")
)

args = parser.parse_args()

spn_auth = args.spn_auth
capacity_name = args.capacity
admin_upns = args.admin_upns

if admin_upns:
    admin_upns = [upn.strip() for upn in admin_upns.split(",")]

def download_zip(url, dest_path):
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete.")

def extract_zip(zip_path, extract_to):
    print(f"Extracting {zip_path} to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

def find_executable(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".exe"):
                return os.path.join(root, file)
    raise FileNotFoundError("No .exe file found in the extracted zip.")

def run_executable(exe_path, args):
    print(f"Running: {exe_path} {' '.join(args)}")
    result = subprocess.run([exe_path] + args, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)

def main():
    zip_url = "https://github.com/NatVanG/PBI-InspectorV2/releases/download/v2.4.0/win-x64-CLI.zip"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "app.zip")
        extract_path = os.path.join(temp_dir, "extracted")

        download_zip(zip_url, zip_path)
        extract_zip(zip_path, extract_path)

        exe_path = find_executable(extract_path)
        run_executable(exe_path, ["--help"])  # Replace with your actual arguments

main()
