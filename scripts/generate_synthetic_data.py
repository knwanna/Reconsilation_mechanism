import pandas as pd
from faker import Faker
import random

faker = Faker()

def generate_synthetic_data(n_records: int, output_path: str) -> None:
    """Generate a synthetic dataset of publication records with controlled noise.

    Args:
        n_records: Number of records to generate.
        output_path: Path to save the CSV file.
    """
    data = []
    authors = [faker.name() for _ in range(100)]
    titles = [faker.sentence(nb_words=3).strip(".") for _ in range(200)]
    
    for i in range(n_records):
        title = random.choice(titles)
        author = random.choice(authors)
        year = random.randint(1800, 2025)
        canonical_id = f"{author.replace(' ', '-').lower()}-{i}"
        
        # Introduce noise (10% chance of misspelling or variation)
        if random.random() < 0.1:
            title = title[:-1] + random.choice('aeiou')  # Misspell title
        elif random.random() < 0.1:
            author = author.split()[0]  # Use only first name
        elif random.random() < 0.05:
            title = title[:len(title)//2]  # Truncate title
        
        data.append({
            "id": i + 1,
            "title": title,
            "author": author,
            "year": year,
            "canonical_id": canonical_id
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated {n_records} records at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data(1000, "data/synthetic_literary_works.csv")
