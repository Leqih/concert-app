import { useEffect, useState } from 'react';
import { fallbackShows } from './fallback';
import { fetchCityShows } from './ticketmaster';
import type { DataSource, Show } from './types';

const API_KEY = process.env.EXPO_PUBLIC_TM_API_KEY;

export function useShows(city = 'New York') {
  const [shows, setShows] = useState<Show[]>(fallbackShows);
  const [source, setSource] = useState<DataSource>('fallback');
  const [loading, setLoading] = useState(Boolean(API_KEY));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!API_KEY) return;
    let cancelled = false;
    setLoading(true);
    fetchCityShows(API_KEY, city)
      .then((live) => {
        if (cancelled || live.length === 0) return;
        setShows(live);
        setSource('ticketmaster');
      })
      .catch((e: unknown) => {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [city]);

  return { shows, source, loading, error };
}
