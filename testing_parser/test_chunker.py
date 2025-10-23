from embedding.chunker import Chunker, STANDARD_CATEGORIES
import numpy as np

chunker = Chunker(STANDARD_CATEGORIES)

pdf_path = "embedding/company_licitations/BBTT Obras Anillos RCI Estanques_General_8Tks_ORE-23BB.O24 RevB2_opt.pdf"

import os

# Generate chunks from the PDF
pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
chunks = chunker.generate_chunks(pdf_path=pdf_path, licitation_id=pdf_name, document_name=pdf_name)

for chunk in chunks:
    print(f"Chunk Heading: {chunk.heading}")
    print(f"Chunk size: {len(chunk.content)} characters")
    print(f"Chunk Content: {chunk.content}...\n")

chunk_lengths = [len(c.content) for c in chunks]
print(f"Total chunks: {len(chunks)}")
print(f"Min chunk length: {min(chunk_lengths)} characters")
print(f"Max chunk length: {max(chunk_lengths)} characters")
print(f"Average chunk length: {sum(chunk_lengths) / len(chunk_lengths):.2f} characters")
print(f"Standard Deviation of chunk lengths: {np.std(chunk_lengths):.2f} characters")

print("Graphical representation of chunk lengths:")

import matplotlib.pyplot as plt

ordered_lengths = sorted(chunk_lengths)

print(ordered_lengths)

plt.figure(figsize=(10, 6))
plt.hist(ordered_lengths, bins=30, color='blue', alpha=0.7)
plt.title("Distribution of Chunk Lengths")
plt.xlabel("Chunk Length (characters)")
plt.ylabel("Frequency")
plt.grid(axis='y', alpha=0.75)
plt.show()

# Output markdown file where each chunk is a section with metadata
# out_path = f"testing_parser/exports/{pdf_name}_chunks.md"
# with open(out_path, "w", encoding="utf-8") as f:
# 	for i, c in enumerate(chunks, start=1):
# 		# Header with chunk number and heading
# 		heading = c.heading or "No Heading"
# 		f.write(f"# Chunk {i}, {heading}\n\n")

# 		# Metadata (category, licitation_id, document_name, content length)
# 		metadata = {
# 			"category": getattr(c, "category", ""),
# 			"licitation_id": getattr(c, "licitation_id", ""),
# 			"document_name": getattr(c, "document_name", ""),
# 			"content_length": len(getattr(c, "content", "")),
# 		}
# 		for k, v in metadata.items():
# 			f.write(f"- {k}: {v}\n")
# 		f.write("\n")

# 		# Content
# 		f.write(getattr(c, "content", "") + "\n\n")

# print(f"Saved chunks markdown to: {out_path}")