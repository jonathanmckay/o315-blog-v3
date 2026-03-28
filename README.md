# Jonathan McKay - Blog

Personal blog built with Hugo, sourced from the o314 journal archive.

## Structure

- **Source entries:** `../YYYY/*.md` (o314 journal entries)
- **Blog posts:** `content/posts/*.md` (published blog posts)
- **Linking:** Blog posts link to source entries, source entries link back via `published:` frontmatter field

## Local Development

```bash
hugo server --buildDrafts
```

Visit http://localhost:1313/

## Deployment

GitHub Actions auto-deploys to GitHub Pages on push to `main`.

## Publishing Workflow

1. Select entry from o314 journal
2. Create blog post in `content/posts/`
3. Add source link at bottom: `**Source:** [o314/YYYY/filename.md](../../YYYY/filename.md)`
4. Add backlink to source entry frontmatter: `published: "[[blog/content/posts/YYYY-MM-slug.md|Blog: Title]]"`
5. Commit and push

## Domain

- Production: https://jonathanmckay.com
- Substack signup: https://jonathanmckay.substack.com
