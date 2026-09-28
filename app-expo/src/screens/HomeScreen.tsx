import { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, Linking, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather, Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Poster } from '../components/Poster';
import { placeholderBuddyStats } from '../data/buddies';
import { useShows } from '../data/useShows';
import type { Show } from '../data/types';
import { colors, fonts, gradient, space } from '../theme';
import { dateRange, price } from '../utils/format';

const CATEGORIES = [
  { label: 'Concerts', icon: 'microphone-variant' as const, dark: false },
  { label: 'Festivals', icon: 'tent' as const, dark: false },
  { label: 'Live House', icon: 'speaker' as const, dark: false },
  { label: 'Find a Buddy', icon: 'account-group' as const, dark: true },
];
const TABS = ['FOR YOU', 'NEARBY', 'FOLLOWING'] as const;
const GENRES = ['All', 'Pop', 'Rock', 'Hip-Hop/Rap', 'R&B', 'Dance/Electronic', 'Latin'] as const;
const CREW_WINDOW_SECONDS = 6 * 3600 + 19 * 60 + 16;

function pad(n: number) {
  return String(n).padStart(2, '0');
}

export function HomeScreen() {
  const insets = useSafeAreaInsets();
  const { shows, source, loading, error } = useShows('New York');
  const [dropIndex, setDropIndex] = useState(0);
  const [secs, setSecs] = useState(CREW_WINDOW_SECONDS);
  const [tab, setTab] = useState<(typeof TABS)[number]>('FOR YOU');
  const [genre, setGenre] = useState<(typeof GENRES)[number]>('All');

  useEffect(() => {
    const t = setInterval(() => setSecs((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(t);
  }, []);

  const drops = shows.slice(0, 3);
  const drop = drops[dropIndex % Math.max(drops.length, 1)];
  const hotTours = useMemo(
    () => shows.filter((s) => !drops.includes(s)).sort((a, b) => b.moreDates.length - a.moreDates.length).slice(0, 3),
    [shows, drops],
  );
  const justAdded = shows[shows.length - 1];
  const buddyShow = hotTours[0];
  const feed = useMemo(
    () => shows.filter((s) => !drops.includes(s)).filter((s) => genre === 'All' || s.genre === genre).slice(0, 8),
    [shows, genre, drops],
  );

  const countdown = `${pad(Math.floor(secs / 3600))} : ${pad(Math.floor((secs % 3600) / 60))} : ${pad(secs % 60)}`;

  return (
    <View style={styles.root}>
      <ScrollView contentContainerStyle={{ paddingBottom: 110 + insets.bottom }} showsVerticalScrollIndicator={false}>
        {/* Header: logo + city search + categories, on the brand gradient */}
        <LinearGradient colors={[colors.red, colors.red, colors.cyan]} locations={[0, 0.18, 1]} style={[styles.header, { paddingTop: insets.top + 14 }]}>
          <View style={styles.headerRow}>
            <Text style={styles.logo}>
              PLUS{'\n'}ONE<Text style={{ color: colors.white }}>+</Text>
            </Text>
            <View style={styles.search}>
              <Pressable style={styles.city} accessibilityRole="button" accessibilityLabel="Change city">
                <Text style={styles.cityText}>New York</Text>
                <Ionicons name="caret-down" size={10} color={colors.ink} />
              </Pressable>
              <TextInput placeholder="Shows, bands" placeholderTextColor={colors.muted} style={styles.searchInput} accessibilityLabel="Search shows" />
              <Pressable style={styles.searchBtn} accessibilityRole="button">
                <Feather name="search" size={14} color={colors.white} />
                <Text style={styles.searchBtnText}>Search</Text>
              </Pressable>
            </View>
          </View>
          <View style={styles.categories}>
            {CATEGORIES.map((c) => (
              <Pressable key={c.label} style={styles.category} accessibilityRole="button">
                <View style={[styles.sticker, c.dark && styles.stickerDark]}>
                  <MaterialCommunityIcons name={c.icon} size={28} color={c.dark ? colors.cyan : colors.red} />
                </View>
                <Text style={styles.categoryText}>{c.label}</Text>
              </Pressable>
            ))}
          </View>
        </LinearGradient>

        <View style={styles.body}>
          {/* This week's ticket drop */}
          {drop ? (
            <View style={styles.drop}>
              <View style={styles.dropHead}>
                <LinearGradient colors={gradient} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.dropPill}>
                  <Ionicons name="flash" size={15} color={colors.ink} />
                  <Text style={styles.dropPillText}>THIS WEEK'S TICKET DROP</Text>
                </LinearGradient>
                <Pressable onPress={() => setDropIndex((i) => i + 1)} style={styles.shuffle} accessibilityRole="button" accessibilityLabel="Show another">
                  <Ionicons name="shuffle" size={16} color={colors.white} />
                </Pressable>
              </View>
              <View style={styles.dropCard}>
                <View style={{ flex: 1, gap: 6 }}>
                  <Text style={styles.dropTitle} numberOfLines={3}>{drop.title}</Text>
                  <Text style={styles.muted}>{dateRange(drop.date, drop.moreDates)}</Text>
                  <Text style={styles.redStrong}>{drop.venue}</Text>
                  {price(drop.priceFrom, drop.currency) ? <Text style={styles.muted}>From <Text style={styles.priceBig}>{price(drop.priceFrom, drop.currency)}</Text></Text> : null}
                </View>
                <Poster imageUrl={drop.imageUrl} name={drop.artist} width={108} height={112} badge={`${placeholderBuddyStats(drop).waiting.toLocaleString()} waiting`} />
              </View>
              <View style={styles.dropFoot}>
                <View style={{ flexDirection: 'row', alignItems: 'baseline', gap: 8 }}>
                  <Text style={styles.countdown}>{countdown}</Text>
                  <Text style={styles.countdownLabel}>left to join a crew</Text>
                </View>
                <Pressable onPress={() => drop.ticketUrl && Linking.openURL(drop.ticketUrl)} accessibilityRole="button">
                  <LinearGradient colors={gradient} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.cta}>
                    <Text style={styles.ctaText}>{drop.ticketUrl ? 'Tickets' : 'Set alert'}</Text>
                  </LinearGradient>
                </Pressable>
              </View>
            </View>
          ) : null}

          {/* Hot tours / Just added / Buddy plaza */}
          <View style={styles.grid}>
            <View style={[styles.tile, { flex: 1 }]}>
              <View style={styles.tileHead}>
                <Text style={styles.tileTitle}>HOT TOURS</Text>
                <Feather name="chevron-right" size={16} color={colors.ink} />
              </View>
              {hotTours.map((s, i) => (
                <View key={s.id} style={styles.miniRow}>
                  <Poster imageUrl={s.imageUrl} name={s.artist} width={40} height={50} radius={8} />
                  {i === 0 ? <Text style={styles.top1}>TOP 1</Text> : null}
                  <View style={{ flex: 1 }}>
                    <Text style={styles.miniTitle} numberOfLines={2}>{s.title}</Text>
                    <Text style={styles.miniMeta} numberOfLines={1}>{s.venue} · {dateRange(s.date, s.moreDates)}</Text>
                  </View>
                </View>
              ))}
            </View>
            <View style={{ flex: 1, gap: space.gap }}>
              {justAdded ? (
                <View style={[styles.tile, { flex: 1 }]}>
                  <View style={styles.tileHead}>
                    <Text style={styles.tileTitle}>JUST ADDED</Text>
                    <Text style={styles.blackTag}>NEW</Text>
                  </View>
                  <View style={styles.miniRow}>
                    <Poster imageUrl={justAdded.imageUrl} name={justAdded.artist} width={40} height={50} radius={8} />
                    <View style={{ flex: 1 }}>
                      <Text style={styles.miniTitle} numberOfLines={2}>{justAdded.artist}</Text>
                      <Text style={styles.miniMeta} numberOfLines={1}>{dateRange(justAdded.date, justAdded.moreDates)}</Text>
                    </View>
                  </View>
                </View>
              ) : null}
              {buddyShow ? (
                <LinearGradient colors={gradient} style={[styles.tile, { flex: 1 }]}>
                  <View style={styles.tileHead}>
                    <Text style={styles.tileTitleSm} numberOfLines={1}>BUDDY PLAZA</Text>
                    <Text style={styles.blackTag}>HOT</Text>
                  </View>
                  <Text style={styles.hashtag} numberOfLines={1}>
                    #{buddyShow.artist.replace(/\s+/g, '')} {placeholderBuddyStats(buddyShow).crewFilled}/{placeholderBuddyStats(buddyShow).crewSize}
                  </Text>
                  <View style={styles.joinBar}>
                    <Text style={styles.joinText}>Crew forming — join</Text>
                    <Feather name="chevron-right" size={13} color={colors.ink} />
                  </View>
                </LinearGradient>
              ) : null}
            </View>
          </View>

          {/* Feed */}
          <View style={styles.tabs}>
            {TABS.map((t) => (
              <Pressable key={t} onPress={() => setTab(t)} accessibilityRole="tab" accessibilityState={{ selected: tab === t }}>
                <Text style={tab === t ? styles.tabOn : styles.tabOff}>{t}</Text>
                {tab === t ? <View style={styles.tabMark} /> : null}
              </Pressable>
            ))}
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginHorizontal: -space.gutter }} contentContainerStyle={{ paddingHorizontal: space.gutter, gap: 8 }}>
            {GENRES.map((g) => (
              <Pressable key={g} onPress={() => setGenre(g)} style={[styles.chip, genre === g && styles.chipOn]} accessibilityRole="button" accessibilityState={{ selected: genre === g }}>
                <Text style={[styles.chipText, genre === g && { color: colors.white }]}>{g}</Text>
              </Pressable>
            ))}
          </ScrollView>

          {loading ? <ActivityIndicator color={colors.redText} style={{ marginTop: 12 }} /> : null}
          {feed.length === 0 && !loading ? <Text style={[styles.muted, { textAlign: 'center', paddingVertical: 20 }]}>No {genre} shows coming up yet.</Text> : null}
          {feed.map((s) => (
            <FeedItem key={s.id} show={s} />
          ))}

          <Text style={styles.sourceNote}>
            {source === 'ticketmaster'
              ? 'Event data and images powered by Ticketmaster.'
              : error
                ? `Couldn't reach Ticketmaster (${error}). Showing the built-in list of real NYC shows.`
                : 'Showing the built-in list of real NYC shows. Add a Ticketmaster API key for live data and event images.'}
          </Text>
        </View>
      </ScrollView>

      <BottomNav bottomInset={insets.bottom} />
    </View>
  );
}

function FeedItem({ show }: { show: Show }) {
  const stats = placeholderBuddyStats(show);
  const p = price(show.priceFrom, show.currency);
  return (
    <Pressable style={styles.feedItem} onPress={() => show.ticketUrl && Linking.openURL(show.ticketUrl)} accessibilityRole="link">
      <Poster imageUrl={show.imageUrl} name={show.artist} width={108} height={136} radius={14} badge={`${(stats.waiting / 1000).toFixed(1)}K waiting`} />
      <View style={{ flex: 1, gap: 6, paddingTop: 2 }}>
        <Text style={styles.feedTitle} numberOfLines={3}>{show.title}</Text>
        <Text style={styles.muted} numberOfLines={1}>{dateRange(show.date, show.moreDates)} · {show.venue}</Text>
        {p ? <Text style={styles.muted}><Text style={styles.redStrong}>{p}</Text> from</Text> : null}
        <View style={styles.buddyPill}>
          <Text style={styles.buddyPillText}>{stats.lookingForBuddy} looking for a buddy</Text>
        </View>
      </View>
    </Pressable>
  );
}

function BottomNav({ bottomInset }: { bottomInset: number }) {
  const item = (label: string, icon: keyof typeof Feather.glyphMap, active = false) => (
    <Pressable style={styles.navItem} accessibilityRole="tab" accessibilityState={{ selected: active }}>
      <Feather name={icon} size={22} color={active ? colors.redText : colors.muted} />
      <Text style={[styles.navText, active && { color: colors.redText, fontFamily: fonts.bodyHeavy }]}>{label}</Text>
    </Pressable>
  );
  return (
    <View style={[styles.nav, { paddingBottom: 12 + bottomInset }]}>
      {item('Home', 'home', true)}
      {item('Explore', 'compass')}
      <Pressable accessibilityRole="button" accessibilityLabel="Post">
        <LinearGradient colors={gradient} style={styles.post}>
          <Feather name="camera" size={22} color={colors.ink} />
          <Text style={styles.postText}>POST</Text>
        </LinearGradient>
      </Pressable>
      {item('Tickets', 'credit-card')}
      {item('Me', 'user')}
    </View>
  );
}

const sticker = { borderWidth: 2, borderColor: colors.ink, boxShadow: `3px 3px 0px ${colors.ink}` };

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.white },
  header: { paddingHorizontal: space.gutter, paddingBottom: 20, gap: 18 },
  headerRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  logo: { fontFamily: fonts.display, fontSize: 24, lineHeight: 24, color: colors.ink },
  search: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 8, height: 46, paddingLeft: 12, paddingRight: 5, borderRadius: 14, backgroundColor: colors.white },
  city: { flexDirection: 'row', alignItems: 'center', gap: 3 },
  cityText: { fontFamily: fonts.bodyHeavy, fontSize: 13, color: colors.ink },
  searchInput: { flex: 1, minWidth: 0, fontFamily: fonts.body, fontSize: 13, color: colors.ink, paddingVertical: 0 },
  searchBtn: { height: 36, paddingHorizontal: 11, borderRadius: 10, backgroundColor: colors.ink, flexDirection: 'row', alignItems: 'center', gap: 5 },
  searchBtnText: { fontFamily: fonts.bodyHeavy, fontSize: 13, color: colors.white },
  categories: { flexDirection: 'row', justifyContent: 'space-between' },
  category: { alignItems: 'center', gap: 6, flex: 1 },
  sticker: { width: 60, height: 60, borderRadius: 20, backgroundColor: colors.white, alignItems: 'center', justifyContent: 'center', ...sticker },
  stickerDark: { backgroundColor: colors.ink, boxShadow: `3px 3px 0px ${colors.white}` },
  categoryText: { fontFamily: fonts.bodyHeavy, fontSize: 12, color: colors.ink },

  body: { paddingHorizontal: space.gutter, paddingTop: 16, gap: 14 },
  muted: { fontFamily: fonts.body, fontSize: 13, color: colors.muted },
  redStrong: { fontFamily: fonts.bodyHeavy, fontSize: 13, color: colors.redText },
  priceBig: { fontFamily: fonts.display, fontSize: 20, color: colors.redText },

  drop: { padding: 12, borderRadius: 22, backgroundColor: colors.ink, gap: 10 },
  dropHead: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  dropPill: { flexDirection: 'row', alignItems: 'center', gap: 6, height: 34, paddingHorizontal: 12, borderRadius: 10 },
  dropPillText: { fontFamily: fonts.display, fontSize: 16, color: colors.ink },
  shuffle: { width: 38, height: 38, borderRadius: 19, borderWidth: 1.5, borderColor: colors.white, alignItems: 'center', justifyContent: 'center' },
  dropCard: { flexDirection: 'row', gap: 10, padding: 12, borderRadius: 16, backgroundColor: colors.white },
  dropTitle: { fontFamily: fonts.bodyHeavy, fontSize: 16, lineHeight: 20, color: colors.ink },
  dropFoot: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 2 },
  countdown: { fontFamily: fonts.display, fontSize: 24, color: colors.white, fontVariant: ['tabular-nums'] },
  countdownLabel: { fontFamily: fonts.body, fontSize: 12, color: '#C8C8D0' },
  cta: { height: 40, paddingHorizontal: 16, borderRadius: 20, alignItems: 'center', justifyContent: 'center' },
  ctaText: { fontFamily: fonts.bodyHeavy, fontSize: 13, color: colors.ink },

  grid: { flexDirection: 'row', gap: space.gap },
  tile: { padding: 12, borderRadius: space.radius, backgroundColor: colors.surface, gap: 10 },
  tileHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  tileTitle: { fontFamily: fonts.display, fontSize: 18, color: colors.ink },
  tileTitleSm: { fontFamily: fonts.display, fontSize: 16, color: colors.ink, flexShrink: 1 },
  hashtag: { fontFamily: fonts.bodyHeavy, fontSize: 13, color: colors.ink },
  blackTag: { flexShrink: 0, fontFamily: fonts.bodyHeavy, fontSize: 11, color: colors.white, backgroundColor: colors.ink, paddingHorizontal: 7, paddingVertical: 3, borderRadius: 7, overflow: 'hidden' },
  miniRow: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  top1: { position: 'absolute', left: -4, top: -6, fontFamily: fonts.bodyHeavy, fontSize: 9, color: colors.white, backgroundColor: colors.ink, paddingHorizontal: 4, paddingVertical: 1, borderRadius: 4, overflow: 'hidden' },
  miniTitle: { fontFamily: fonts.bodyHeavy, fontSize: 12, lineHeight: 15, color: colors.ink },
  miniMeta: { fontFamily: fonts.body, fontSize: 11, color: colors.muted, marginTop: 2 },
  joinBar: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 8, paddingVertical: 6, borderRadius: 8, backgroundColor: 'rgba(255,255,255,0.8)' },
  joinText: { fontFamily: fonts.bodyBold, fontSize: 11, color: colors.ink },

  tabs: { flexDirection: 'row', alignItems: 'flex-end', gap: 16, paddingTop: 6 },
  tabOn: { fontFamily: fonts.display, fontSize: 26, color: colors.ink },
  tabOff: { fontFamily: fonts.display, fontSize: 18, color: colors.subtle, paddingBottom: 3 },
  tabMark: { position: 'absolute', left: 0, right: 0, bottom: 5, height: 8, backgroundColor: colors.cyan, zIndex: -1 },
  chip: { height: 36, paddingHorizontal: 14, borderRadius: 18, backgroundColor: colors.surface, justifyContent: 'center' },
  chipOn: { backgroundColor: colors.ink },
  chipText: { fontFamily: fonts.bodyBold, fontSize: 13, color: colors.ink },

  feedItem: { flexDirection: 'row', gap: 12 },
  feedTitle: { fontFamily: fonts.bodyHeavy, fontSize: 17, lineHeight: 21, color: colors.ink },
  buddyPill: { alignSelf: 'flex-start', paddingHorizontal: 9, paddingVertical: 4, borderRadius: 999, backgroundColor: colors.redTint },
  buddyPillText: { fontFamily: fonts.bodyHeavy, fontSize: 12, color: colors.redTintText },
  sourceNote: { fontFamily: fonts.body, fontSize: 11, color: colors.subtle, textAlign: 'center', paddingTop: 8 },

  nav: { position: 'absolute', left: 0, right: 0, bottom: 0, flexDirection: 'row', justifyContent: 'space-around', alignItems: 'flex-end', paddingTop: 8, backgroundColor: colors.white, borderTopWidth: 1.5, borderTopColor: '#ECECEF' },
  navItem: { alignItems: 'center', justifyContent: 'center', gap: 3, minWidth: 56, minHeight: 48 },
  navText: { fontFamily: fonts.body, fontSize: 11, color: colors.muted },
  post: { width: 64, height: 64, marginBottom: 4, borderRadius: 20, alignItems: 'center', justifyContent: 'center', gap: 1, ...sticker },
  postText: { fontFamily: fonts.bodyHeavy, fontSize: 11, color: colors.ink },
});
