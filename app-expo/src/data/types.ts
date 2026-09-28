/** A show as the app uses it, whatever the source. */
export type Show = {
  id: string;
  artist: string;
  title: string;
  venue: string;
  city: string;
  /** ISO date, e.g. 2026-11-21 */
  date: string;
  /** Extra dates at the same venue (multi-night runs), ISO. */
  moreDates: string[];
  /** Best-fitting official event image from the API, if any. */
  imageUrl?: string;
  genre?: string;
  priceFrom?: number;
  currency?: string;
  ticketUrl?: string;
};

export type DataSource = 'ticketmaster' | 'fallback';
