/**
 * Simple API logging utility for development
 *
 * Logs HTTP requests, responses, and errors to console in development mode.
 * All logs are disabled in production builds.
 */

const isDev = import.meta.env.DEV;

/**
 * Format duration in milliseconds to readable string
 */
function formatDuration(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

/**
 * Sanitize data for logging (remove sensitive fields)
 */
function sanitize(data: unknown): unknown {
  if (!data || typeof data !== 'object') return data;

  const sanitized = { ...data } as Record<string, unknown>;
  const sensitiveFields = ['password', 'token', 'authorization', 'cookie'];

  Object.keys(sanitized).forEach(key => {
    if (sensitiveFields.includes(key.toLowerCase())) {
      sanitized[key] = '[REDACTED]';
    }
  });

  return sanitized;
}

/**
 * Log outgoing API request
 */
export function logRequest(method: string, url: string, data?: unknown): void {
  if (!isDev) return;

  const sanitizedData = data ? sanitize(data) : null;
  const logData = sanitizedData ? ` ${JSON.stringify(sanitizedData)}` : '';

  console.log(`[API] → ${method} ${url}${logData}`);
}

/**
 * Log successful API response
 */
export function logResponse(
  method: string,
  url: string,
  status: number,
  duration: number
): void {
  if (!isDev) return;

  console.log(`[API] ← ${status} ${method} ${url} (${formatDuration(duration)})`);
}

/**
 * Log API error
 */
export function logError(
  method: string,
  url: string,
  status: number | null,
  message: string,
  duration?: number
): void {
  if (!isDev) return;

  const statusStr = status || 'ERR';
  const durationStr = duration ? ` (${formatDuration(duration)})` : '';

  console.error(`[API] ✗ ${statusStr} ${method} ${url}${durationStr} - ${message}`);
}
