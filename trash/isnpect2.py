import subprocess
import sys
import time


def capture_process_snapshot(pid):
    """
    Capture a snapshot of the running Python process with the given PID
    and display the stack trace along with local variables.
    """
    try:
        # Full path to py-spy (update with the correct path you got from 'which py-spy')
        py_spy_path = "/home/luis/.local/bin/py-spy"  # Replace with the correct path

        # Run py-spy with elevated permissions (sudo)
        result = subprocess.run(
            ["sudo", "env", "PATH=$PATH:/usr/local/bin",
                "py-spy", "dump", "--pid", str(pid)],
            capture_output=True,
            text=True
        )

        # Check if py-spy ran successfully
        if result.returncode == 0:
            print("Process Snapshot:")
            print(result.stdout)
        else:
            print(f"Error capturing process snapshot:\n{result.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_process.py <PID>")
        sys.exit(1)

    pid = sys.argv[1]

    try:
        # Validate that the PID is an integer
        pid = int(pid)
        print(f"Attaching to process with PID: {pid}")

        # Capture a snapshot of the process every few seconds
        while True:
            capture_process_snapshot(pid)
            time.sleep(5)  # Adjust the frequency as needed

    except ValueError:
        print("Invalid PID. Please provide a numeric process ID.")
