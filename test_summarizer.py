
from summarizer import summarize_text

text = """
Trees are important for our environment.
Trees absorb carbon dioxide and release oxygen.
Trees provide food and shelter for animals.
Deforestation increases global warming.
Planting trees helps protect nature.
"""

summary = summarize_text(text, 2)

print("ORIGINAL TEXT:")
print(text)

print("\nGENERATED SUMMARY:")
print(summary)
