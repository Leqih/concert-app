export const colors = {
  red: '#FF292B',
  cyan: '#01E9FF',
  ink: '#111114',
  white: '#FFFFFF',
  surface: '#F4F4F6',
  line: '#E4E4E8',
  muted: '#5E5E6A',
  subtle: '#8A8A96',
  // Accent text on white: pure #FF292B is too light for small text, so use a deeper red.
  redText: '#D40F12',
  redTint: '#FFE3E3',
  redTintText: '#B00D10',
} as const;

// Vertical red → cyan, as in the brand reference (the midpoint turns a soft grey naturally).
export const gradient = [colors.red, colors.cyan] as const;

export const fonts = {
  display: 'Oswald_700Bold',
  body: 'Manrope_500Medium',
  bodyBold: 'Manrope_700Bold',
  bodyHeavy: 'Manrope_800ExtraBold',
} as const;

export const space = { gutter: 14, gap: 10, radius: 18 } as const;
