import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding.cohere_embedder import CohereEmbedder
import time

# --- Configurable Variables ---
CSV_FILE_PATH = "licitation_filter/UNGM_UNSPSC_21-Oct-2025. - UNSPSC.csv"  # The path to your products CSV
ROWS_TO_PROCESS = 13283
TARGET_TERMS = [
    "Engineering",
    "Construction",
    "Civil Works",
    "Piping",
    "Electricity",
    "Industrial Maintenance"
]

products = [
    # Core Services
    "Engineering",
    "Construction",
    "Civil Works",
    "EPC",
    "Potable Water",
    "Trenching",
    "Water Systems",

    # Key Industries
    "Mining",
    "Energy",
    "Steel",
    "Cement",
    "Water",

    # Specific Technical Services
    "Instrumentation",
    "Telemetry",
    "SCADA",
    "Technical Specifications",

    # Consulting & Management Services
    "Consulting",
    "Project Management",
    "Feasibility Studies",
    "Scoping Studies",
    "Risk Analysis",
    "Peer Review",
    "Procurement"
]
# ------------------------------

def run_semantic_test():
    
    # 1. Initialize your embedder
    # We don't pass a model, so it will use the defaults in your class
    # (e.g., embed-v4.0, which will likely fail without 'input_type'
    # and gracefully fall back to 'embed-english-v2.0' as you defined)
    embedder = CohereEmbedder()
    
    # Check if the client initialized correctly
    if embedder.client is None:
        print("="*50)
        print("ERROR: Cohere client not initialized.")
        print("Please ensure your COHERE_TRIAL_API_KEY is set in a .env file.")
        print("="*50)
        return

    # 2. Read product names from the CSV file
    product_names = []
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= ROWS_TO_PROCESS:
                    print(f"\nReached limit of {ROWS_TO_PROCESS} rows.")
                    break
                if row:
                    product_names.append(row[-1].strip()) # Get last column
                    if row[-1].strip() in products:
                        print(f"{row[-2].strip()},")
    except FileNotFoundError:
        print("="*50)
        print(f"ERROR: CSV file not found at '{CSV_FILE_PATH}'")
        print("Please create this file and add product data to it.")
        print("="*50)
        return
    except Exception as e:
        print(f"An error occurred reading the CSV: {e}")
        return

    if not product_names:
        print("No product names found in the CSV file.")
        return

    print(f"\nSuccessfully read {len(product_names)} product names from CSV.")
    print(f"Target Terms: {TARGET_TERMS}\n")

    # 3. Embed both lists (using the batch-capable _embed_texts method)
    print("Generating embeddings with Cohere...")
    
    # Embed target terms
    print("Embedding target terms...")
    target_embeddings = embedder._embed_texts(TARGET_TERMS)
    print("Target term embeddings generated.\n")
    
   # Embed product names in batches
    print(f"Embedding {len(product_names)} products in batches...")
    product_embeddings_list = []  # A temp list to store results
    batch_size = 4000
    
    for i in range(0, len(product_names), batch_size):
        # Create a batch of 4000 names
        batch_names = product_names[i : i + batch_size]
        
        print(f"  Processing batch {i // batch_size + 1} ({len(batch_names)} items)...")
        batch_embeddings = embedder._embed_texts(batch_names)
        product_embeddings_list.extend(batch_embeddings)
        
        # Check if this is NOT the last batch
        if i + batch_size < len(product_names):
            print(f"  ...Success. Sleeping for 10 seconds to avoid rate limit.")
            time.sleep(10)
            
    print("All product embeddings generated.\n")

    # 4. Calculate cosine similarity
    # Convert lists of embeddings to numpy arrays for sklearn
    target_embeddings_np = np.array(target_embeddings)
    product_embeddings_np = np.array(product_embeddings_list)
    
    sim_matrix = cosine_similarity(product_embeddings_np, target_embeddings_np)

    
    # 5. Visualize the results

    product_averages = []
    print("--- Semantic Similarity Results ---")
    
    for i, product_name in enumerate(product_names):
        # Get the row of scores for this product
        product_scores = sim_matrix[i]
        
        # Calculate the average score
        average_score = np.mean(product_scores)
        product_averages.append((product_name, average_score))
        
        
        # Combine terms and scores to visualize them
        scores_with_terms = list(zip(TARGET_TERMS, product_scores))
        
        # Sort by score (highest first)
        scores_with_terms.sort(key=lambda item: item[1], reverse=True)
        
        # Print the breakdown
        for term, score in scores_with_terms:
            print(f"  {term:>25}: {score:.4f}")

    # 6. Summary of top matches
    product_averages.sort(key=lambda item: item[1], reverse=True)
    print("\n=== Top Products by Average Similarity ===")
    for product_name, avg_score in product_averages[:1000]:
        print(f"{product_name}: {avg_score:.4f}")

    
if __name__ == "__main__":
    run_semantic_test()
