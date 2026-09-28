import { useState } from 'react';
import { Image, StyleSheet, Text, View, type ViewStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, fonts, gradient } from '../theme';
import { initials } from '../utils/format';

type Props = {
  imageUrl?: string;
  name: string;
  width: number;
  height: number;
  radius?: number;
  /** Small black badge in the top-left corner, e.g. "6,243 waiting". */
  badge?: string;
  style?: ViewStyle;
  children?: React.ReactNode;
};

/** Official event image when the API gives one; otherwise a brand-gradient poster with initials. */
export function Poster({ imageUrl, name, width, height, radius = 12, badge, style, children }: Props) {
  const [failed, setFailed] = useState(false);
  const showImage = Boolean(imageUrl) && !failed;

  return (
    <View style={[{ width, height, borderRadius: radius, overflow: 'hidden' }, style]}>
      {showImage ? (
        <Image
          source={{ uri: imageUrl }}
          style={StyleSheet.absoluteFill}
          resizeMode="cover"
          onError={() => setFailed(true)}
          accessibilityLabel={name}
        />
      ) : (
        <LinearGradient colors={gradient} start={{ x: 0, y: 0.1 }} end={{ x: 0, y: 0.9 }} style={[StyleSheet.absoluteFill, styles.fallback]}>
          <Text style={[styles.initials, { fontSize: Math.round(width / 3.4) }]}>{initials(name)}</Text>
        </LinearGradient>
      )}
      {badge ? (
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{badge}</Text>
        </View>
      ) : null}
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  fallback: { justifyContent: 'flex-end', padding: 8 },
  initials: { fontFamily: fonts.display, color: colors.ink, lineHeight: undefined },
  badge: { position: 'absolute', left: 6, top: 6, paddingHorizontal: 7, paddingVertical: 3, borderRadius: 7, backgroundColor: colors.ink },
  badgeText: { fontFamily: fonts.bodyHeavy, fontSize: 11, color: colors.white },
});
