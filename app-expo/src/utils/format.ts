/** "Nov 21 – Nov 22" / "Dec 1" / "15 nights · Oct 2 – Oct 31" */
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export function shortDate(iso: string): string {
  const [, m, d] = iso.split('-').map(Number);
  return `${MONTHS[m - 1]} ${d}`;
}

export function dateRange(first: string, more: string[]): string {
  if (more.length === 0) return shortDate(first);
  const last = [...more].sort().at(-1)!;
  const nights = more.length + 1;
  const range = `${shortDate(first)} – ${shortDate(last)}`;
  return nights > 2 ? `${nights} nights · ${range}` : range;
}

export function initials(name: string): string {
  const words = name.replace(/^the\s+/i, '').split(/\s+/).filter(Boolean);
  return (words.length > 1 ? words[0][0] + words[1][0] : name.slice(0, 2)).toUpperCase();
}

export function price(from?: number, currency?: string): string | null {
  if (from == null) return null;
  const sym = currency === 'USD' || !currency ? '$' : `${currency} `;
  return `${sym}${Math.round(from)}`;
}
