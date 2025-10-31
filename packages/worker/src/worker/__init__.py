from worker.config import WorkerConfigLoader, WorkerConfig


def main() -> None:
    loader: WorkerConfig = WorkerConfigLoader()
    config = loader.load()
    print(config)
    print("Hello from worker!")
