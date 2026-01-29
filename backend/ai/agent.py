import re

def agent(text: str):
    # Extract name
    name_match = re.search(r"dr\.?\s+([A-Za-z]+)", text, re.I)
    hcp_name = "Dr " + name_match.group(1) if name_match else ""

    # Extract date
    date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
    interaction_date = date_match.group(0) if date_match else ""

    # Sentiment
    sentiment = "Positive" if "positive" in text.lower() else "Neutral"

    # Follow-up
    follow_up = ""
    if "send" in text.lower():
        follow_up = "Send brochure"

    # Summary
    summary = text.split(".")[0]

    return {
        "hcp_name": hcp_name,
        "interaction_date": interaction_date,
        "notes": text,
        "sentiment": sentiment,
        "follow_up": follow_up,
        "summary": summary
    }
