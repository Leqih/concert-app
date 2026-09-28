# Plus One — concert buddy app (Home screen)

Expo (React Native, TypeScript) app. Home screen follows the Figma home layout, in English,
with the white + red→cyan brand gradient.

## Run it

```bash
npm install
cp .env.example .env        # then paste your Ticketmaster key into .env
npx expo start              # press i / a for a simulator, or scan the QR code with Expo Go
npx expo start --web        # or run it in the browser
```

## Real data and images

- **With a Ticketmaster API key** (free at https://developer.ticketmaster.com — sign up, create an app,
  copy the *Consumer Key*): the app loads upcoming New York music events from the
  Discovery API, including the official event images, venues, dates and price ranges.
  Multi-night runs (e.g. a 15-night residency) are merged into one card.
- **Without a key**, or if the API can't be reached: it shows a built-in list of real NYC shows
  (Madison Square Garden and Barclays Center calendars, checked Sept 2026), with gradient
  posters instead of photos and no prices.

Keep the "powered by Ticketmaster" note if you ship with their data; check their terms of use.

## Not real yet

Buddy numbers ("x waiting", "x looking for a buddy", crew slots) and the crew countdown come from
`src/data/buddies.ts`, a stable placeholder until Plus One's own backend exists.

## Structure

```
App.tsx                      fonts + safe area, renders Home
src/screens/HomeScreen.tsx   the Home screen
src/components/Poster.tsx    event image, or brand-gradient fallback
src/data/ticketmaster.ts     Discovery API client
src/data/useShows.ts         loads live shows, falls back to the built-in list
src/data/fallback.ts         real NYC shows used without a key
src/data/buddies.ts          placeholder buddy stats
src/theme.ts                 colors, gradient, fonts
```

Next step when more screens arrive: move to Expo Router (`src/app/`) for navigation.
