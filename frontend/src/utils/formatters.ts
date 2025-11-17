/**
 * Utility formatters for displaying data in a user-friendly format
 */

/**
 * Formats a number as currency in USD
 *
 * @param value - The number to format
 * @returns Formatted currency string (e.g., "$45,000")
 *
 * @example
 * ```ts
 * formatCurrency(45000) // "$45,000"
 * formatCurrency(1234.56) // "$1,235"
 * ```
 */
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

/**
 * Formats a date string to a readable format
 *
 * @param dateString - ISO date string
 * @returns Formatted date string (e.g., "Jan 15, 2024")
 *
 * @example
 * ```ts
 * formatDate('2024-01-15') // "Jan 15, 2024"
 * ```
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(date);
};

/**
 * Formats a number with thousand separators
 *
 * @param value - The number to format
 * @returns Formatted number string (e.g., "1,234")
 *
 * @example
 * ```ts
 * formatNumber(1234) // "1,234"
 * formatNumber(1234567) // "1,234,567"
 * ```
 */
export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US').format(value);
};

/**
 * Formats a date string to relative time
 *
 * @param dateString - ISO date string or null
 * @param prefix - Optional prefix text (e.g., "Created", "Started", "Completed")
 * @returns Formatted relative time string (e.g., "Created 2 hours ago")
 *
 * @example
 * ```ts
 * formatRelativeTime('2024-01-15T10:00:00Z', 'Created') // "Created 2 hours ago"
 * formatRelativeTime('2024-01-15T10:00:00Z') // "2 hours ago"
 * ```
 */
export const formatRelativeTime = (dateString: string | null, prefix?: string): string => {
  if (!dateString) return '';

  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };

  for (const [unit, seconds] of Object.entries(intervals)) {
    const interval = Math.floor(diffInSeconds / seconds);
    if (interval >= 1) {
      const formatter = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
      const relativeTime = formatter.format(-interval, unit as Intl.RelativeTimeFormatUnit);
      return prefix ? `${prefix} ${relativeTime}` : relativeTime;
    }
  }

  const justNow = 'just now';
  return prefix ? `${prefix} ${justNow}` : justNow;
};
