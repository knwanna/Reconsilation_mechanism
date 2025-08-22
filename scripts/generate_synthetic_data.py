import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_synthetic_data(n=1000):
    data = []
    authors = [fake.name() for _ in range(50)]
    for i in range(1, n + 1):
        title = fake.sentence(nb_words=3).strip('.')
        author = random.choice(authors)
        year = random.randint(1800, 2025)
        canonical_id = f"{author.replace(' ', '-').lower()}-{i}"
        data.append([i, title, author, year, canonical_id])
    df = pd.DataFrame(data, columns=['id', 'title', 'author', 'year', 'canonical_id'])
    df.to_csv('data/synthetic_literary_works.csv', index=False)

if __name__ == '__main__':
    generate_synthetic_data()
