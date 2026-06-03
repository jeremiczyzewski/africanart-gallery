import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const ROOT = path.join(process.cwd(), 'content');

export type Exhibit = {
  slug: string;
  title: string;
  image: string;
  imageAlt: string;
  pdfUrl: string;
  pdfLabel: string;
  prevSlug: string;
  nextSlug: string;
  metadata: string;
  body: string;
  shortDescription: string;
};

function parseExhibit(file: string): Exhibit {
  const raw = fs.readFileSync(path.join(ROOT, 'exhibits', file), 'utf-8');
  const { data, content } = matter(raw);
  const lines = (data.metadata || '').split('\n').filter(Boolean);
  // Pierwsza linia metadata jako short desc na karcie galerii nie ma sensu; zamiast tego biore pierwsze zdanie body
  const shortDescription = (content || '').split('\n').filter(Boolean)[0]?.slice(0, 160) || '';
  return {
    slug: data.slug,
    title: data.title || '',
    image: data.image || '',
    imageAlt: data.imageAlt || '',
    pdfUrl: data.pdfUrl || '',
    pdfLabel: data.pdfLabel || 'Pobierz dokumentację PDF',
    prevSlug: data.prevSlug || '',
    nextSlug: data.nextSlug || '',
    metadata: data.metadata || '',
    body: content.trim(),
    shortDescription,
  };
}

export function getExhibits(lang: 'pl' | 'en-us' = 'pl'): Exhibit[] {
  const dir = path.join(ROOT, 'exhibits');
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter(f => f.endsWith(`_${lang}.md`))
    .map(parseExhibit)
    .sort((a, b) => a.title.localeCompare(b.title, 'pl'));
}

export function getExhibit(slug: string, lang: 'pl' | 'en-us' = 'pl'): Exhibit | null {
  const file = `${slug}_${lang}.md`;
  const full = path.join(ROOT, 'exhibits', file);
  if (!fs.existsSync(full)) return null;
  return parseExhibit(file);
}

function readJSON(rel: string) {
  const full = path.join(ROOT, rel);
  if (!fs.existsSync(full)) return null;
  return JSON.parse(fs.readFileSync(full, 'utf-8'));
}

export function getFooter(lang: 'pl' | 'en-us' = 'pl') {
  const j = readJSON(`settings/footer_${lang}.json`);
  if (!j) return null;
  const p = j.slices?.[0]?.primary || {};
  return {
    phone: p.phone?.[0] || null,
    email: p.email?.[0] || null,
    address: p.address?.[0] || null,
    socialMedia: p.socialMedia?.[0] || null,
    openingHours: p.openingHours?.[0] || null,
  };
}

export function getNavigation(lang: 'pl' | 'en-us' = 'pl') {
  const j = readJSON(`settings/navigation_${lang}.json`);
  if (!j) return [];
  return (j.links || []).map((l: any) => ({
    label: l.label?.[0]?.text || '',
    slug: l.link?.uid || l.link?.slug || '',
  }));
}

export function getSocial(lang: 'pl' | 'en-us' = 'pl') {
  const j = readJSON(`settings/social_media_navigation_${lang}.json`);
  if (!j) return [];
  return (j.navigation_item || []).map((it: any) => ({
    label: it.label,
    url: it.link?.url || '#',
    iconAlt: it.icon?.alt || it.label,
  }));
}

function rtToText(rt: any): string {
  if (!Array.isArray(rt)) return '';
  return rt.map((b: any) => b.text || '').join('\n').trim();
}

export function getHomeHero(lang: 'pl' | 'en-us' = 'pl') {
  const j = readJSON(`pages/home_${lang}.json`);
  if (!j) return null;
  const slice = j.slices?.[0]?.primary || {};
  const photos = (slice.photos || []).map((p: any) => ({
    url: p.image?.url || '',
    alt: p.image?.alt || '',
  })).filter((p: any) => p.url);
  return {
    title: slice.title || '',
    backgroundImage: slice.backgroundImage?.url || '',
    backgroundAlt: slice.backgroundImage?.alt || '',
    photos,
    buttonText: slice.buttonLink?.text || 'Zobacz więcej',
    buttonSlug: slice.buttonLink?.uid || 'gallery',
  };
}

export function getPage(slug: string, lang: 'pl' | 'en-us' = 'pl') {
  const j = readJSON(`pages/${slug}_${lang}.json`);
  if (!j) return null;
  return {
    title: rtToText(j.title),
    slices: j.slices || [],
  };
}
