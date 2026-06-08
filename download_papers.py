import arxiv
import os
import time

DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)

queries = [
    "large language model",
    "transformer architecture",
    "retrieval augmented generation",
    "attention mechanism deep learning"
]

downloaded = set(os.listdir(DATA_FOLDER))

client = arxiv.Client()

for query in queries:

    print(f"\nSearching for: {query}\n")

    search = arxiv.Search(
        query=query,
        max_results=75,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for result in client.results(search):

        filename = result.title.replace(" ", "_") + ".pdf"

        if filename in downloaded:
            continue

        print("Downloading:", result.title)

        try:
            result.download_pdf(dirpath=DATA_FOLDER, filename=filename)
            downloaded.add(filename)

            time.sleep(3)  # prevents arXiv rate limit

        except Exception as e:
            print("Failed:", e)