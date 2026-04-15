#!/usr/bin/env python3
"""
Basic usage example: classify a task → route → call Anthropic API with scaffold.

Requires:
  - Anthropic API key (ANTHROPIC_API_KEY env var)
  - Ollama running with nomic-embed-text
  - anthropic package installed

Usage:
  python examples/basic_usage.py
"""

import os
import sys
import json

# Import the router
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from router import ClaudeRouter


def main():
    # 1. Initialize the router (loads centroids, routing table, scaffolds)
    print("Initializing router...")
    try:
        router = ClaudeRouter()
    except Exception as e:
        print(f"Router init failed: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return

    # 2. Define a task to evaluate
    task = "Evaluate this research paper for methodological rigor and novelty"
    print(f"\nTask: {task}\n")

    # 3. Route the task (embedding → centroid match → lookup table)
    print("Routing...")
    try:
        route = router.route(task)
    except Exception as e:
        print(f"Routing failed: {e}")
        return

    # 4. Show the routing decision
    print(f"   Category:     {route['category']}")
    print(f"   Model:        {route['model']}")
    print(f"   Scaffold:     {route['scaffold_key'] or '(none)'}")
    print(f"   Confidence:   {route['confidence']:.4f}")
    print(f"   Cost/1K:      ${route['cost_per_1k']:.4f}")

    if route["low_confidence"]:
        print("   Low confidence -- consider manual review")

    # 5. Build the scaffolded prompt
    print("\nBuilding prompt with scaffold...\n")
    prompt = router.build_prompt(task, route)
    if route["scaffold_text"]:
        print("--- SCAFFOLDED PROMPT ---")
        print(prompt)
        print("--- END PROMPT ---\n")

    # 6. Call Anthropic API with the scaffold
    print("Calling Anthropic API...")
    try:
        from anthropic import Anthropic
    except ImportError:
        print("anthropic package not installed")
        print("   Install: pip install anthropic")
        return

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set")
        return

    client = Anthropic(api_key=api_key)

    # Dummy research paper for demo
    research_text = """
    Title: Attention Is All You Need

    This paper introduces the Transformer architecture, using self-attention mechanisms
    to process sequences in parallel rather than sequentially. Training time improved
    40% and BLEU scores on translation improved to 28.4 on the WMT 2014 dataset.
    """

    try:
        response = client.messages.create(
            model=route["model"],
            max_tokens=500,
            system=route["scaffold_text"] if route["scaffold_text"] else None,
            messages=[
                {
                    "role": "user",
                    "content": f"{task}\n\n{research_text}",
                }
            ],
        )
        print("Response received\n")
        print(response.content[0].text)
    except Exception as e:
        print(f"API call failed: {e}")
        return

    # 7. Show cost comparison
    print("\nCost comparison:")
    haiku_cost = (len(f"{task}{research_text}") / 1000) * 0.0008
    sonnet_cost = (len(f"{task}{research_text}") / 1000) * 0.003
    opus_cost = (len(f"{task}{research_text}") / 1000) * 0.015
    routed_cost = (len(f"{task}{research_text}") / 1000) * route["cost_per_1k"]

    print(f"   Haiku:     ${haiku_cost:.4f}")
    print(f"   Sonnet:    ${sonnet_cost:.4f}")
    print(f"   Opus:      ${opus_cost:.4f}")
    print(f"   Routed:    ${routed_cost:.4f} ({route['model']})")
    print(f"   Savings:   {((opus_cost - routed_cost) / opus_cost * 100):.0f}% vs Opus")


if __name__ == "__main__":
    main()
