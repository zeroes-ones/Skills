#!/usr/bin/env python3
"""Token budget checker — validates prompt + expected completion fits within model limits.

Usage: python check_token_budget.py --prompt prompt.txt --model gpt-4o --max-output 4096
"""

import argparse
import sys
import json

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

# Model context window limits (tokens)
MODEL_LIMITS = {
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16384,
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "claude-3.5-sonnet": 200000,
    "gemini-1.5-pro": 2000000,
    "gemini-1.5-flash": 1000000,
    "text-embedding-3-small": 8191,
    "text-embedding-3-large": 8191,
    "text-embedding-ada-002": 8191,
    "bge-large-en": 512,
    "voyage-2": 32000,
}

# Model → tiktoken encoding mapping
MODEL_ENCODING = {
    "gpt-4o": "o200k_base",
    "gpt-4o-mini": "o200k_base",
    "gpt-4": "cl100k_base",
    "gpt-4-turbo": "cl100k_base",
    "gpt-4-32k": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "gpt-3.5-turbo-16k": "cl100k_base",
    "text-embedding-3-small": "cl100k_base",
    "text-embedding-3-large": "cl100k_base",
    "text-embedding-ada-002": "cl100k_base",
}


def count_tokens(text: str, model: str) -> int:
    """Count tokens in text for given model."""
    if not TIKTOKEN_AVAILABLE:
        # Fallback: ~4 chars per token
        return len(text) // 4

    encoding_name = MODEL_ENCODING.get(model)
    if encoding_name:
        try:
            enc = tiktoken.get_encoding(encoding_name)
            return len(enc.encode(text))
        except Exception:
            pass
    # Fallback: cl100k_base
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


def main():
    parser = argparse.ArgumentParser(description="Check prompt fits within model token budget")
    parser.add_argument("--prompt", required=True, help="File containing the prompt text")
    parser.add_argument("--model", required=True, help="Model name (e.g., gpt-4o, claude-3-opus)")
    parser.add_argument("--max-output", type=int, default=4096,
                       help="Expected max output tokens (default: 4096)")
    parser.add_argument("--system-prompt", help="Optional system prompt file")
    parser.add_argument("--overhead", type=int, default=50,
                       help="Token overhead for message formatting (default: 50)")
    parser.add_argument("--budget", type=int, help="Override model context window limit")
    args = parser.parse_args()

    with open(args.prompt) as f:
        prompt_text = f.read()

    system_text = ""
    if args.system_prompt:
        with open(args.system_prompt) as f:
            system_text = f.read()

    model_limit = args.budget or MODEL_LIMITS.get(args.model)
    if not model_limit:
        print(f"ERROR: Unknown model '{args.model}'. Known models: {', '.join(sorted(MODEL_LIMITS.keys()))}")
        print(f"Use --budget to specify a custom token limit.")
        sys.exit(2)

    prompt_tokens = count_tokens(prompt_text, args.model)
    system_tokens = count_tokens(system_text, args.model) if system_text else 0
    total_input = prompt_tokens + system_tokens + args.overhead
    total_with_output = total_input + args.max_output

    print("=" * 55)
    print("TOKEN BUDGET CHECK")
    print("=" * 55)
    print(f"Model:              {args.model}")
    print(f"Context window:     {model_limit:,} tokens")
    print()
    print(f"System prompt:      {system_tokens:,} tokens")
    print(f"User prompt:        {prompt_tokens:,} tokens")
    print(f"Message overhead:   {args.overhead:,} tokens (estimated)")
    print(f"Input total:        {total_input:,} tokens")
    print(f"Max output:         {args.max_output:,} tokens")
    print(f"Total with output:  {total_with_output:,} tokens")
    print()
    print(f"Buffer:             {model_limit - total_with_output:,} tokens "
          f"({(1 - total_with_output/model_limit)*100:.1f}% remaining)")
    print(f"{'=' * 55}")

    if total_with_output <= model_limit:
        print("VERDICT: WITHIN BUDGET ✅")
        print(f"  {model_limit - total_with_output:,} tokens remaining for additional context or longer output")
        sys.exit(0)
    else:
        excess = total_with_output - model_limit
        print(f"VERDICT: OVER BUDGET ❌ — exceeds by {excess:,} tokens")
        print()
        print("Recommendations:")
        print(f"  1. Reduce prompt by {excess:,} tokens ({(excess/prompt_tokens*100):.0f}% of prompt)")
        print(f"  2. Or reduce --max-output from {args.max_output:,} to {args.max_output - excess:,}")
        print(f"  3. Or use a larger context model (available: {model_limit * 2:,}+)")

        if args.model in MODEL_ENCODING:
            # Show approximate character reduction needed
            chars_to_cut = excess * 4
            print(f"\n  Approximate characters to remove: ~{chars_to_cut:,} characters")
        sys.exit(1)


if __name__ == "__main__":
    main()
