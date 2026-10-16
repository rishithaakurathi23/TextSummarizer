
from flask import Flask, render_template, request
from summarizer import summarize_text
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    original_text = ""
    summary = ""

    original_words = 0
    summary_words = 0
    compression = 0

    original_sentences = 0
    summary_sentences = 0

    original_reading_time = 0
    summary_reading_time = 0

    summary_length = 3
    error = ""

    if request.method == "POST":
        original_text = request.form.get("text", "").strip()

        # Get the selected summary length
        try:
            summary_length = int(
                request.form.get("summary_length", 3)
            )
        except (ValueError, TypeError):
            summary_length = 3

        # Allow only supported summary lengths
        allowed_lengths = [1, 2, 3, 5, 10, 15, 20]

        if summary_length not in allowed_lengths:
            summary_length = 3

        # Validate the input text
        if not original_text:
            error = "Please enter some text to summarize."

        elif len(original_text.split()) < 10:
            error = "Please enter at least 10 words to generate a summary."

        else:
            # Generate the summary
            summary = summarize_text(
                original_text, summary_length
            )

            # Calculate word counts
            original_words = len(
                re.findall(r"\b\w+\b", original_text)
            )

            summary_words = len(
                re.findall(r"\b\w+\b", summary)
            )

            # Calculate sentence counts
            original_sentences = len(
                re.findall(r"[.!?]+", original_text)
            )

            summary_sentences = len(
                re.findall(r"[.!?]+", summary)
            )

            # Estimate reading time at 200 words per minute
            if original_words > 0:
                original_reading_time = max(
                    1, (original_words + 199) // 200
                )

            if summary_words > 0:
                summary_reading_time = max(
                    1, (summary_words + 199) // 200
                )

            # Calculate compression percentage
            if original_words > 0:
                compression = round(
                    (1 - summary_words / original_words) * 100,
                    2
                )

    return render_template(
        "index.html",
        original_text=original_text,
        summary=summary,
        original_words=original_words,
        summary_words=summary_words,
        compression=compression,
        summary_length=summary_length,
        original_sentences=original_sentences,
        summary_sentences=summary_sentences,
        original_reading_time=original_reading_time,
        summary_reading_time=summary_reading_time,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
