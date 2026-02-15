#!/usr/bin/env python3
"""Post a daily tweet as a reply chain off the pinned post."""

import os
import random
import subprocess
import sys
import time

from requests_oauthlib import OAuth1Session

REPO = "greynewell/evaldriven.org"
URL = "https://evaldriven.org"

TEMPLATES = [
    "{count} developers have signed the Eval-Driven Development manifesto. Join them: {url}",
    "Eval-driven development: deterministic, automated evaluation as a first-class engineering practice. {count} signatories and counting. {url}",
    "If you ship AI without evals, you're shipping blind. {count} developers agree. Read the manifesto: {url}",
    "Every AI system deserves deterministic evals. {count} signatories so far — add your name: {url}",
    "The Eval-Driven Development manifesto now has {count} signatories. Star the repo to sign: {url}",
]


def get_stargazer_count():
    """Get stargazer count via gh CLI."""
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}", "--jq", ".stargazers_count"],
        capture_output=True, text=True, timeout=30,
    )
    return int(result.stdout.strip())


def post_tweet(text, reply_to_id=None):
    """Post a tweet via X API v2, optionally as a reply."""
    oauth = OAuth1Session(
        os.environ["X_API_KEY"],
        client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    payload = {"text": text}
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

    resp = oauth.post("https://api.x.com/2/tweets", json=payload)
    if resp.status_code != 201:
        print(f"Tweet failed ({resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)
    tweet_id = resp.json()["data"]["id"]
    print(f"Posted tweet {tweet_id}")
    return tweet_id


def main():
    # Random delay so posts aren't always at exactly the same time
    delay = random.randint(60, 900)
    print(f"Waiting {delay}s before posting...")
    time.sleep(delay)

    count = get_stargazer_count()
    print(f"Current stargazer count: {count}")

    reply_to_id = os.environ.get("PINNED_TWEET_ID", "")
    if reply_to_id:
        print(f"Replying to pinned tweet: {reply_to_id}")
    else:
        print("No PINNED_TWEET_ID set — posting standalone", file=sys.stderr)
        reply_to_id = None

    template = random.choice(TEMPLATES)
    text = template.format(count=count, url=URL)
    print(f"Tweet: {text}")

    post_tweet(text, reply_to_id)


if __name__ == "__main__":
    main()
