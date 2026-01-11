type BrandShade = 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;

export const brandGreen: Record<BrandShade, string> = {
  50: '#e4fbf3',
  100: '#c6f5e4',
  200: '#95e9ce',
  300: '#6fddbb',
  400: '#55d1aa',
  500: '#57ebb8',
  600: '#2aa07f',
  700: '#1f7a60',
  800: '#165646',
  900: '#0f3429',
};

export const BRAND_PRIMARY = brandGreen[500];
export const BRAND_ACCENT = brandGreen[600];
export const BRAND_PRIMARY_DARK = brandGreen[700];
export const BRAND_PRIMARY_DEEP = brandGreen[900];
export const BRAND_PRIMARY_SOFT = brandGreen[100];
export const BRAND_PRIMARY_SURFACE = brandGreen[50];

export const brandGradient = {
  from: '#07110f',
  via: '#0b1a16',
  to: '#57ebb8',
} as const;
