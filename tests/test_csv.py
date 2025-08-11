import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.repositories.csv_repository import CSVPublicationRepository

def test_csv_loading():
    try:
        print("\nTesting CSV Repository...")
        repo = CSVPublicationRepository("data/literary_works.csv")
        
        print(f"✅ Successfully loaded {len(repo.data)} publications")
        print("Sample records:")
        for i, pub in enumerate(repo.data[:3]):
            print(f"  {i+1}. {pub.title} (ID: {pub.id})")
            
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_csv_loading()