import os
from time import time
import pytest


def run_pytest_with_env(env_vars):
    # Set environment variables
    os.environ.update(env_vars)

    # Run pytest programmatically
    return pytest.main([])


def run_pytest_with_multiple_envs(env_compositions):
    for idx, env_vars in enumerate(env_compositions):
        print(f"\nRunning pytest with environment composition {idx + 1}:")
        for key, value in env_vars.items():
            print(f"{key}: {value}")

        # Run pytest with the current environment configuration
        result = run_pytest_with_env(env_vars)
        print(f"\nPytest run {idx + 1} completed with exit code: {result}")


if __name__ == "__main__":
    # Define different environment compositions
    now = time()
    env_compositions = [
        {
            "LONG_DATASET_SKIP": "2",
            "OFFSET_DATASET": "0",
            "MAX_VARIETY": "2",
            "OFFSET_VARIETY": str(x),
        }
        for x in range(0, 10, 2)
    ] + [
        {
            "LONG_DATASET_SKIP": "2",
            "OFFSET_DATASET": "1",
            "MAX_VARIETY": "2",
            "OFFSET_VARIETY": str(x),
        }
        for x in range(0, 10, 2)
    ]

    # Run pytest with each environment composition
    run_pytest_with_multiple_envs(env_compositions)
    print(f"\nFull test finished at {round(time()-now,2)}s")
