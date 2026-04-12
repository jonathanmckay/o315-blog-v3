#!/usr/bin/env python3
"""Sync review files from the vault to the blog content directory.

Copies reviews from ~/vault/hcmc/reviews/ (year-nested) to
content/reviews/ (flat), skipping non-review files. The blog's
_index.md cascade handles layout assignment.

Usage:
  cd ~/vault/hcmp/o315/blog
  python3 scripts/sync-vault-reviews.py --dry-run
  python3 scripts/sync-vault-reviews.py
"""

import argparse
import os
import re
import shutil
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_ROOT = os.path.dirname(SCRIPT_DIR)
CONTENT_REVIEWS = os.path.join(BLOG_ROOT, "content", "reviews")
VAULT_REVIEWS = os.path.normpath(os.path.join(BLOG_ROOT, "..", "..", "..", "hcmc", "reviews"))

# Files and directories to skip entirely
SKIP_FILES = {"batch_move.py", "low-score-audit.md", "reviews.md"}


def parse_frontmatter(filepath):
    """Parse YAML frontmatter. Returns (dict, raw_content) or (None, raw_content)."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except (OSError, IOError):
        return None, ""

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
        return fm, content
    except yaml.YAMLError:
        return None, content


def strip_layout_field(content):
    """Remove layout: review from frontmatter if present (cascade handles it)."""
    return re.sub(r"^layout:\s*review\s*\n", "", content, count=1, flags=re.MULTILINE)


def has_body_content(filepath):
    """Check if a review has actual content after the frontmatter."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except (OSError, IOError):
        return False
    match = re.match(r"^---\s*\n.*?\n---\s*\n?", content, re.DOTALL)
    if not match:
        return False
    body = content[match.end():].strip()
    # A bare URL alone doesn't count as content
    if not body or (body.startswith("http") and "\n" not in body.strip()):
        return False
    return True


def is_review_file(filepath, filename):
    """Check if a file should be synced as a review."""
    if filename in SKIP_FILES:
        return False
    if not filename.endswith(".md"):
        return False

    fm, _ = parse_frontmatter(filepath)
    if not isinstance(fm, dict):
        return False

    # Skip index files (year indexes like 2024.md)
    if fm.get("type") == "index":
        return False

    # Skip no-publish reviews
    tags = fm.get("tags", []) or []
    if "no-publish" in tags:
        return False

    # Must be a review
    if fm.get("type") != "review":
        return False

    # Skip empty reviews (no body content)
    if not has_body_content(filepath):
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Sync vault reviews to blog content")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--verbose", action="store_true", help="Show unchanged files too")
    args = parser.parse_args()

    if not os.path.isdir(VAULT_REVIEWS):
        print(f"Error: vault reviews not found at {VAULT_REVIEWS}")
        return 1

    # Collect vault reviews: slug -> source path
    vault_reviews = {}
    for dirpath, _dirnames, filenames in os.walk(VAULT_REVIEWS):
        for fn in filenames:
            filepath = os.path.join(dirpath, fn)
            if is_review_file(filepath, fn):
                if fn in vault_reviews:
                    print(f"  Warning: slug collision: {fn} (keeping {vault_reviews[fn]})")
                else:
                    vault_reviews[fn] = filepath

    print(f"Found {len(vault_reviews)} reviews in vault")

    # Sync to blog
    added = 0
    updated = 0
    unchanged = 0

    for slug, src_path in sorted(vault_reviews.items()):
        dst_path = os.path.join(CONTENT_REVIEWS, slug)
        _, src_content = parse_frontmatter(src_path)
        src_content = strip_layout_field(src_content)

        if os.path.isfile(dst_path):
            with open(dst_path, "r", encoding="utf-8", errors="replace") as f:
                existing = f.read()
            if existing == src_content:
                unchanged += 1
                if args.verbose:
                    print(f"  unchanged: {slug}")
                continue
            action = "update"
            updated += 1
        else:
            action = "add"
            added += 1

        prefix = "[dry-run] " if args.dry_run else ""
        print(f"  {prefix}{action}: {slug}")

        if not args.dry_run:
            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(src_content)

    # Remove orphans (blog files not in vault)
    removed = 0
    for fn in sorted(os.listdir(CONTENT_REVIEWS)):
        if fn == "_index.md":
            continue
        if not fn.endswith(".md"):
            continue
        if fn not in vault_reviews:
            removed += 1
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"  {prefix}remove: {fn}")
            if not args.dry_run:
                os.remove(os.path.join(CONTENT_REVIEWS, fn))

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
    print(f"  Added: {added}")
    print(f"  Updated: {updated}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Removed: {removed}")


if __name__ == "__main__":
    main()
