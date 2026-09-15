import os
import sys
import subprocess

print("--- Starting Supervisor ---")

# Run app.py if it exists
if os.path.exists("app.py"):
    print("Found app.py. Starting bot process...")
    subprocess.run([sys.executable, "app.py"])
else:
    print("Error: app.py was not found in root directory!")
