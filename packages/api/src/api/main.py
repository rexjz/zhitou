

from api.config import APIConfigLoader

def main():
  loader = APIConfigLoader()
  config: APIConfigLoader = loader.load()
  print(config)

if __name__ == "__main__":
  main()