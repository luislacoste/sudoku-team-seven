import psutil

# Find the Python process you're interested in by inspecting attributes
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    cmdline = proc.info.get('cmdline')
    if cmdline and 'test2.py' in cmdline:
        pid = proc.info['pid']
        print(f"Found process: PID={pid}")

        # Get memory information
        try:
            process = psutil.Process(pid)
            mem_info = process.memory_info()
            print(f"Memory usage for PID {pid} ({cmdline}):")
            print(f"py-spy top --pid {pid}")
            quit()
            print(f"  RSS (Resident Set Size): {
                  mem_info.rss / (1024 * 1024):.2f} MB")
            print(f"  VMS (Virtual Memory Size): {
                  mem_info.vms / (1024 * 1024):.2f} MB")
            print(f"  Shared Memory: {mem_info.shared / (1024 * 1024):.2f} MB")
            print(f"  Text (code): {mem_info.text / (1024 * 1024):.2f} MB")
            print(f"  Data + Stack: {mem_info.data / (1024 * 1024):.2f} MB")
            print(f"  Libs: {mem_info.lib / (1024 * 1024):.2f} MB")
            print(f"  Dirty Pages: {mem_info.dirty / (1024 * 1024):.2f} MB")
        except psutil.NoSuchProcess:
            print("Process no longer exists.")
        except Exception as e:
            print(f"An error occurred: {e}")



