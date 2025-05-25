import os

FIFO_PATH = "/tmp/serv2_fifo"

try:
    with open(FIFO_PATH, "r") as fifo:
        data = fifo.read()
        print(f"Fecha y hora: {data}")
except FileNotFoundError:
    print("No abre")
except Exception as e:
    print(f"No lee: {e}")