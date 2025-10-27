#! /usr/bin/env python3

import argparse
import random
import string

def generate_random_string(length=24, exclude_chars=""):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    if exclude_chars:
        all_chars = ''.join(char for char in all_chars if char not in exclude_chars)
    
    if len(all_chars) == 0:
        raise ValueError("All characters are excluded, cannot generate a random string.")
    
    return ''.join(random.choice(all_chars) for _ in range(length))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random string.")
    parser.add_argument(
        '-l', '--length', type=int, default=24,
        help="Length of the random string (default: 24, min: 12, max: 32)"
    )
    parser.add_argument(
        '-e', '--exclude', type=str, default="",
        help="Characters to exclude from the random string"
    )

    args = parser.parse_args()
    
    if not 12 <= args.length <= 32:
        raise ValueError("Length must be between 12 and 32.")
    
    random_string = generate_random_string(length=args.length, exclude_chars=args.exclude)
    print(f"Generated random string: {random_string}")
