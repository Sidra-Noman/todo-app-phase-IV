// Design system tokens for consistent styling across the application

export const colors = {
  // Primary colors
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    500: '#6366f1',
    600: '#4f46e5',
    700: '#4338ca',
  },
  // Neutral colors (grays)
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  // Semantic colors
  success: {
    50: '#f0fdf4',
    500: '#10b981',
  },
  error: {
    50: '#fef2f2',
    600: '#dc2626',
  },
  warning: {
    500: '#f59e0b',
  },
  info: {
    500: '#3b82f6',
  },
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
};

export const typography = {
  h1: {
    fontSize: '32px',
    fontWeight: 700,
    lineHeight: '40px',
  },
  h2: {
    fontSize: '24px',
    fontWeight: 700,
    lineHeight: '32px',
  },
  h3: {
    fontSize: '20px',
    fontWeight: 600,
    lineHeight: '28px',
  },
  body: {
    fontSize: '16px',
    fontWeight: 400,
    lineHeight: '24px',
  },
  bodySm: {
    fontSize: '14px',
    fontWeight: 400,
    lineHeight: '20px',
  },
  caption: {
    fontSize: '12px',
    fontWeight: 400,
    lineHeight: '16px',
  },
};

export const transitions = {
  feedback: '200ms',
  navigation: '300ms',
};

export const breakpoints = {
  mobile: '320px',
  tablet: '640px',
  desktop: '1024px',
};

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
};
