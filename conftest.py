import os


def pytest_configure(config):
    # Print environment variables before tests start
    optimisation = int(os.environ.get("LONG_DATASET_SKIP", 2))
    optimisation_offset = int(os.environ.get("OFFSET_DATASET", 0))
    variety = min(int(os.environ.get("MAX_VARIETY", 3)), 10)
    variety_offset = min(int(os.environ.get("OFFSET_VARIETY", 0)), 9)
    print("\nEnvironment Variables Before Tests:")
    print(f"Optimisation: {optimisation},offset at {optimisation_offset}")
    print(f"Variety: {variety},offset at {variety_offset}")
