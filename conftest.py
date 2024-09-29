import os


def pytest_configure(config):
    # Print environment variables before tests start
    optimization = int(os.environ.get("LONG_DATASET_SKIP", 2))
    optimization_offset = int(os.environ.get("OFFSET_DATASET", 0))
    variety = min(int(os.environ.get("MAX_VARIETY", 2)), 10)
    variety_offset = min(int(os.environ.get("OFFSET_VARIETY", 0)), 9)
    print("\nEnvironment Variables Before Tests:")
    print(f"Optimization: {optimization},offset at {optimization_offset}")
    print(f"Variety: {variety},offset at {variety_offset}")
