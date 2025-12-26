#!/usr/bin/env python3
"""
Debug script to check RAGFlow API key and dataset permissions.
"""

from worker.config import WorkerConfigLoader
from ragflow_sdk import RAGFlow
import requests

def main():
    # Load config
    loader = WorkerConfigLoader()
    config = loader.load()

    print("=" * 60)
    print("RAGFlow Permission Debug")
    print("=" * 60)

    # Show configuration
    print(f"\nConfiguration:")
    print(f"  RAGFlow URL: {config.ragflow.url}")
    print(f"  API Key: {config.ragflow.apikey[:8]}...{config.ragflow.apikey[-4:] if len(config.ragflow.apikey) > 12 else '[too short]'}")
    print(f"  Target KB Name: {config.ragflow.kb_name}")

    # Get user info via API
    print(f"\n{'='*60}")
    print("Checking API Key Owner...")
    print("=" * 60)

    try:
        # Make a request to get user info
        rag_flow = RAGFlow(api_key=config.ragflow.apikey, base_url=config.ragflow.url)

        # List all datasets accessible to this API key
        print("\nDatasets accessible with your current API key:")
        print("-" * 60)
        datasets = rag_flow.list_datasets()

        if not datasets:
            print("  No datasets found!")
            print("  This means:")
            print("    - You haven't created any datasets with this API key yet")
            print("    - OR no one has shared datasets with you")
        else:
            for i, ds in enumerate(datasets, 1):
                print(f"\n  {i}. Name: {ds.name}")
                print(f"     ID: {ds.id}")
                # Try to get permission info if available
                if hasattr(ds, 'permission'):
                    print(f"     Permission: {ds.permission}")

                # Check if this is the target KB
                if ds.name == config.ragflow.kb_name:
                    print(f"     ✓ THIS IS YOUR TARGET KB '{config.ragflow.kb_name}'")

        # Check specifically for the target KB
        print(f"\n{'='*60}")
        print(f"Checking for dataset: '{config.ragflow.kb_name}'")
        print("=" * 60)

        target_datasets = rag_flow.list_datasets(name=config.ragflow.kb_name)
        if target_datasets:
            print(f"✓ Found '{config.ragflow.kb_name}' - You have access!")
            ds = target_datasets[0]
            print(f"  ID: {ds.id}")
            if hasattr(ds, 'permission'):
                print(f"  Permission: {ds.permission}")
        else:
            print(f"✗ Dataset '{config.ragflow.kb_name}' not found or not accessible")
            print("\nPossible reasons:")
            print("  1. The dataset doesn't exist yet (will be created on first run)")
            print("  2. The dataset exists but was created by a different API key")
            print("  3. The dataset exists with permission='me' by another user")

            print("\nTrying to create the dataset...")
            try:
                new_ds = rag_flow.create_dataset(name=config.ragflow.kb_name, permission="me")
                print(f"✓ Successfully created dataset '{config.ragflow.kb_name}'")
                print(f"  ID: {new_ds.id}")
            except Exception as e:
                print(f"✗ Failed to create dataset: {e}")
                if "lacks permission" in str(e):
                    print("\n⚠️  PERMISSION CONFLICT DETECTED!")
                    print(f"    Dataset '{config.ragflow.kb_name}' exists but belongs to someone else")
                    print("\n    Solutions:")
                    print(f"      1. Change kb_name in config to something else (e.g., '{config.ragflow.kb_name}_new')")
                    print("      2. Ask the owner to grant you team access")
                    print("      3. Delete the existing dataset (if you have access with another API key)")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. RAGFlow service is running")
        print("  2. API key is valid")
        print("  3. Network connectivity is working")

    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
