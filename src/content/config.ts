import { defineCollection, z } from 'astro:content';

const works = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    order: z.number().default(0),
    summary: z.string().optional(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    defaultThemePalette: z.enum(['ocean', 'crimson', 'amber']).default('ocean'),
    defaultLayoutType: z.enum(['document', 'gallery', 'timeline']).default('document'),
    isDraft: z.boolean().default(false),
  }),
});

const chapters = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string(),
    order: z.number(),
    layoutType: z.enum(['document', 'gallery', 'timeline']).optional(),
    themePalette: z.enum(['ocean', 'crimson', 'amber']).optional(),
    tags: z.array(z.string()).default([]),
    summary: z.string().optional(),
    cover: z.string().optional(),
    isDraft: z.boolean().default(false),
  }),
});

export const collections = { works, chapters };
