import multiprocessing
import subprocess

if __name__ == "__main__":
    # System
    NUM_CORES = multiprocessing.cpu_count()
    NUM_UVI_WORKERS = (2 * NUM_CORES) + 1   # Gunicorn rule-of-thumb 2 * CPUs + 1

    cmd = [
        "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", str(NUM_UVI_WORKERS),
    ]

    subprocess.run(cmd)