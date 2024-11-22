import os
import subprocess
import time
from threading import Thread

# Function to check if the loopback address is set
def check_and_set_loopback(loopback="127.0.0.10"):
    loopback_ips = []
    while loopback not in loopback_ips:
        print(f'Checking if {loopback} is added to loopback interface...')
        loopback_ips = subprocess.check_output(["ifconfig", "lo0"]).decode("utf-8")
        time.sleep(15)
    print(f"{loopback} is ready.")
    '''
    if loopback not in loopback_ips:
        print(f"{loopback} is not added to loopback interface, adding...")
        script = f"""
        tell application "System Events"
            do shell script "ifconfig lo0 alias {loopback} up" with administrator privileges
        end tell
        """
        subprocess.run(["osascript", "-e", script], check=True)
    else:
        print(f"{loopback} is already configured.")
    '''


# Function to count files in the directory
def count_files(directory):
    try:
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return 0

# Function to run a process and monitor it
def run_process(command, index):
    while True:
        try:
            print(f"Starting process {index}: {command} {index}")
            process = subprocess.Popen([command, str(index)])
            process.wait()  # Wait for the process to complete
            print(f"Process {index} terminated. Restarting...")
        except Exception as e:
            print(f"Error running process {index}: {e}")
        time.sleep(5)  # Wait before restarting

# Main daemon logic
def daemon():
    loopback = "127.0.0.10"
    directory = os.path.expanduser("~/Documents/Config/cloudflare-tunnel-rdp/hosts")
    command = os.path.expanduser("~/Developer/Scripts/cloudflare-tunnel-rdp.command")
    
    check_and_set_loopback(loopback)
    file_count = count_files(directory)

    # Add homebrew path to PATH environment variable
    ARM_BREW_PATH = '/opt/homebrew/bin/'
    if os.path.exists(ARM_BREW_PATH):
        os.environ["PATH"] += f":{ARM_BREW_PATH}"

    # Define CFD_RDP_NO_PORT_INCREMENT=1 to prevent port increment
    os.environ["CFD_RDP_NO_PORT_INCREMENT"] = "1"
    
    threads = []
    for i in range(file_count):
        thread = Thread(target=run_process, args=(command, i), daemon=True)
        thread.start()
        threads.append(thread)
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting daemon...")

if __name__ == "__main__":
    daemon()
