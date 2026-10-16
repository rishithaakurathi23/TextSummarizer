
import re


def clean_text(text):
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    # Split sentences after ., !, or ?
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def summarize_text(text, summary_length=3):
    text = clean_text(text)

    if not text:
        return ""

    sentences = split_sentences(text)

    # If input has fewer sentences than requested
    if len(sentences) <= summary_length:
        return " ".join(sentences)

    # Extract words from the text
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    stop_words = {
        "the", "is", "a", "an", "and", "or",
        "of", "to", "in", "on", "for", "are",
        "was", "with", "they", "their", "it",
        "this", "that", "as", "by", "be", "can",
        "from", "have", "has", "were", "will"
    }

    # Calculate word frequencies
    frequencies = {}

    for word in words:
        if word not in stop_words:
            frequencies[word] = frequencies.get(word, 0) + 1

    # Calculate the score of each sentence
    scores = []

    for sentence in sentences:
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b', sentence.lower()
        )

        useful_words = [
            word for word in sentence_words
            if word not in stop_words
        ]

        score = sum(
            frequencies.get(word, 0)
            for word in useful_words
        )

        scores.append(score / max(len(useful_words), 1))

    # Select the requested number of sentences
    important_indices = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True
    )[:summary_length]

    # Keep selected sentences in their original order
    important_indices.sort()

    return " ".join(sentences[i] for i in important_indices)

    return summary
