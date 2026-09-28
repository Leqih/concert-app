import type { Show } from '../data/types';

/**
 * Buddy-matching numbers belong to Plus One's own backend, which doesn't exist yet.
 * Until it does, derive a stable placeholder from the show id so the UI has something
 * to lay out. Replace with real crew counts when the API is built.
 */
function hash(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return h;
}

export function placeholderBuddyStats(show: Show) {
  const h = hash(show.id);
  return {
    waiting: 800 + (h % 9000),
    lookingForBuddy: 6 + (h % 60),
    crewSize: 4,
    crewFilled: 1 + (h % 3),
  };
}
