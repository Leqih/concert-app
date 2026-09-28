import type { Show } from './types';

/**
 * Real New York shows (from the Madison Square Garden and Barclays Center calendars,
 * checked Sept 2026). Used when no Ticketmaster API key is set, or the API call fails.
 * No images or prices here on purpose: those only come from the API.
 */
export const fallbackShows: Show[] = [
  { id: 'fb-doja', artist: 'Doja Cat', title: 'Doja Cat', venue: 'Madison Square Garden', city: 'New York', date: '2026-12-01', moreDates: [], genre: 'Hip-Hop/Rap' },
  { id: 'fb-hood', artist: 'The Neighbourhood', title: 'The Neighbourhood: The Wourld Tour', venue: 'Barclays Center', city: 'Brooklyn', date: '2026-11-21', moreDates: ['2026-11-22'], genre: 'Rock' },
  { id: 'fb-summit', artist: 'John Summit', title: 'John Summit: CTRL ESCAPE Arena Tour', venue: 'Barclays Center', city: 'Brooklyn', date: '2026-11-28', moreDates: ['2026-11-29'], genre: 'Dance/Electronic' },
  { id: 'fb-harry', artist: 'Harry Styles', title: 'Harry Styles with Jamie xx', venue: 'Madison Square Garden', city: 'New York', date: '2026-10-02', moreDates: ['2026-10-03', '2026-10-07', '2026-10-09', '2026-10-10', '2026-10-14', '2026-10-16', '2026-10-17', '2026-10-21', '2026-10-23', '2026-10-24', '2026-10-28', '2026-10-30', '2026-10-31'], genre: 'Pop' },
  { id: 'fb-dmb', artist: 'Dave Matthews Band', title: 'Dave Matthews Band', venue: 'Madison Square Garden', city: 'New York', date: '2026-11-12', moreDates: ['2026-11-13'], genre: 'Rock' },
  { id: 'fb-stevie', artist: 'Stevie Wonder', title: 'Stevie Wonder', venue: 'Madison Square Garden', city: 'New York', date: '2026-11-19', moreDates: [], genre: 'R&B' },
  { id: 'fb-sombr', artist: 'sombr', title: 'sombr with Dove Cameron & Hannah Jadagu', venue: 'Madison Square Garden', city: 'New York', date: '2026-11-23', moreDates: ['2026-11-24'], genre: 'Rock' },
  { id: 'fb-miko', artist: 'Young Miko', title: 'Young Miko: Late Checkout Tour', venue: 'Barclays Center', city: 'Brooklyn', date: '2026-11-05', moreDates: [], genre: 'Latin' },
  { id: 'fb-reyez', artist: 'Jessie Reyez', title: 'Jessie Reyez: A Little Vengeance Tour', venue: 'Barclays Center', city: 'Brooklyn', date: '2026-11-19', moreDates: [], genre: 'R&B' },
  { id: 'fb-bocelli', artist: 'Andrea Bocelli', title: 'Andrea Bocelli', venue: 'Madison Square Garden', city: 'New York', date: '2026-12-16', moreDates: ['2026-12-17'], genre: 'Classical' },
];
