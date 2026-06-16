export interface TocItem {
  depth: number;
  text: string;
  slug: string;
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[\s_]+/g, '-')
    .replace(/[^\p{Letter}\p{Number}\-]/gu, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '') || 'heading';
}

export function buildToc(headings: { depth: number; text: string; slug?: string }[] = []): TocItem[] {
  const out: TocItem[] = [];
  const seen = new Map<string, number>();
  for (const h of headings) {
    if (h.depth < 2 || h.depth > 4) continue;
    let slug = h.slug ?? slugify(h.text);
    if (seen.has(slug)) {
      const n = seen.get(slug)! + 1;
      seen.set(slug, n);
      slug = `${slug}-${n}`;
    } else {
      seen.set(slug, 1);
    }
    out.push({ depth: h.depth, text: h.text, slug });
  }
  return out;
}
