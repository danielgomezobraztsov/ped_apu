import os
import time
from datetime import datetime

FIFO_PATH = "/tmp/serv2_fifo"

# Create the FIFO if it doesn't exist
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

try:
    while True:
        with open(FIFO_PATH, "w") as fifo:
            now = datetime.now()
            datetime_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            fifo.write(datetime_str)
        # Optionally remove the FIFO after use, as in the C code
        os.unlink(FIFO_PATH)
except Exception as e:
    print(f"Error: {e}")