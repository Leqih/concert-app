import type { Show } from './types';

const BASE = 'https://app.ticketmaster.com/discovery/v2/events.json';

type TmImage = { ratio?: string; url: string; width: number; height: number; fallback?: boolean };
type TmEvent = {
  id: string;
  name: string;
  url?: string;
  dates?: { start?: { localDate?: string } };
  images?: TmImage[];
  priceRanges?: { min?: number; currency?: string }[];
  classifications?: { genre?: { name?: string } }[];
  _embedded?: {
    venues?: { name?: string; city?: { name?: string } }[];
    attractions?: { name?: string }[];
  };
};
type TmResponse = { _embedded?: { events?: TmEvent[] } };

/** Prefer a real (non-fallback) portrait-ish or 3:2 image around 640px wide. */
function pickImage(images: TmImage[] = []): string | undefined {
  const real = images.filter((i) => !i.fallback);
  const pool = real.length ? real : images;
  const score = (i: TmImage) => {
    const ratioBonus = i.ratio === '3_2' ? 0 : i.ratio === '4_3' ? 50 : i.ratio === '16_9' ? 120 : 200;
    return Math.abs(i.width - 640) + ratioBonus;
  };
  return [...pool].sort((a, b) => score(a) - score(b))[0]?.url;
}

function toIsoNoMs(d: Date): string {
  return d.toISOString().replace(/\.\d{3}Z$/, 'Z');
}

/**
 * Upcoming music events in one city, soonest first. Multi-night runs of the same
 * attraction at the same venue are merged into one Show with `moreDates`.
 */
export async function fetchCityShows(apiKey: string, city = 'New York', size = 60): Promise<Show[]> {
  const params = new URLSearchParams({
    apikey: apiKey,
    city,
    classificationName: 'music',
    sort: 'date,asc',
    size: String(size),
    startDateTime: toIsoNoMs(new Date()),
  });
  const res = await fetch(`${BASE}?${params.toString()}`);
  if (!res.ok) throw new Error(`Ticketmaster ${res.status}`);
  const json = (await res.json()) as TmResponse;
  const events = json._embedded?.events ?? [];

  const merged = new Map<string, Show>();
  for (const e of events) {
    const venue = e._embedded?.venues?.[0];
    const artist = e._embedded?.attractions?.[0]?.name ?? e.name;
    const date = e.dates?.start?.localDate;
    if (!date) continue;
    const key = `${artist}|${venue?.name ?? ''}`;
    const existing = merged.get(key);
    if (existing) {
      if (!existing.moreDates.includes(date) && existing.date !== date) existing.moreDates.push(date);
      continue;
    }
    const price = e.priceRanges?.[0];
    merged.set(key, {
      id: e.id,
      artist,
      title: e.name,
      venue: venue?.name ?? 'Venue TBA',
      city: venue?.city?.name ?? city,
      date,
      moreDates: [],
      imageUrl: pickImage(e.images),
      genre: e.classifications?.[0]?.genre?.name,
      priceFrom: price?.min,
      currency: price?.currency,
      ticketUrl: e.url,
    });
  }
  return [...merged.values()];
}
