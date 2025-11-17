/**
 * Smart retry configuration for TanStack Query
 *
 * Implements intelligent retry logic that only retries on network/server errors,
 * not on client validation errors.
 */

import type { AxiosError } from 'axios';

/**
 * Determine if an error is retryable
 *
 * Retry on:
 * - Network failures (no response)
 * - Server errors (500, 502, 503, 504)
 * - Request timeout (408)
 * - Rate limit (429) - with backoff
 *
 * Don't retry on:
 * - Client errors (400-499 except 408, 429)
 * - Authentication errors (401, 403)
 */
export function shouldRetry(failureCount: number, error: unknown): boolean {
  const maxRetries = 3;

  if (failureCount >= maxRetries) {
    return false;
  }

  // Handle Axios errors
  if (error && typeof error === 'object' && 'isAxiosError' in error) {
    const axiosError = error as AxiosError;

    // Network error (no response from server)
    if (!axiosError.response) {
      return true;
    }

    const status = axiosError.response.status;

    // Don't retry client errors (except specific cases)
    if (status >= 400 && status < 500) {
      // Retry on timeout and rate limit only
      return status === 408 || status === 429;
    }

    // Retry on server errors
    if (status >= 500) {
      return true;
    }
  }

  // Don't retry unknown errors
  return false;
}

/**
 * Calculate retry delay with exponential backoff
 *
 * Delays:
 * - Attempt 1: 1s
 * - Attempt 2: 2s
 * - Attempt 3: 4s
 * - Max: 30s
 */
export function getRetryDelay(attemptIndex: number): number {
  return Math.min(1000 * 2 ** attemptIndex, 30000);
}

/**
 * Smart retry configuration for mutations (POST, PUT, DELETE)
 *
 * More conservative than queries - only 1 retry to avoid duplicate submissions
 */
export function shouldRetryMutation(failureCount: number, error: unknown): boolean {
  const maxRetries = 1;

  if (failureCount >= maxRetries) {
    return false;
  }

  if (error && typeof error === 'object' && 'isAxiosError' in error) {
    const axiosError = error as AxiosError;

    // Network error only - don't retry on any HTTP error for mutations
    if (!axiosError.response) {
      return true;
    }

    const status = axiosError.response.status;

    // Only retry on gateway errors (temporary server issues)
    return status === 502 || status === 503 || status === 504;
  }

  return false;
}

/**
 * Mutation retry delay - longer to avoid hammering server
 */
export function getMutationRetryDelay(attemptIndex: number): number {
  return Math.min(2000 * 2 ** attemptIndex, 10000);
}
