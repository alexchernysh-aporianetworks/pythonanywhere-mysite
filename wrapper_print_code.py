import subprocess
import sys

script_path = sys.argv[1]

# Run the script and wait for it to finish
process = subprocess.run(['python3', script_path])

# Print the real return code
print(f"[WRAPPER] Return code for {script_path}: {process.returncode}")

# Exit with the same code
sys.exit(process.returncode)
