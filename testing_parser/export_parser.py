from embedding.chunker import Chunker, STANDARD_CATEGORIES

# Hardcoded PDF path - change this to the file you want to convert
PDF_PATH = "embedding/company_licitations/(GS)  Bases_Especiales TBL (16-01-24).pdf"

OUT_PATH = "testing_parser/exports/exported_markdown.html"


def run():
	chunker = Chunker(STANDARD_CATEGORIES)
	print(f"Converting: {PDF_PATH}")
	html = chunker.pdf_to_html(PDF_PATH)
	with open(OUT_PATH, "w", encoding="utf-8") as f:
		f.write(html)
	print(f"Saved HTML to: {OUT_PATH}")


if __name__ == "__main__":
	run()