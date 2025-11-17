/**
 * Mock server entry point
 *
 * Conditionally enables mock server based on environment variable
 */

export async function enableMocking() {
  // Only enable mocking in development and if explicitly requested
  if (import.meta.env.VITE_USE_MOCKS !== 'true') {
    // If mocks are disabled, unregister any existing service worker
    if ('serviceWorker' in navigator) {
      const registrations = await navigator.serviceWorker.getRegistrations();
      for (const registration of registrations) {
        if (registration.active?.scriptURL.includes('mockServiceWorker')) {
          console.log('[MSW] Unregistering mock service worker');
          await registration.unregister();
        }
      }
    }
    return;
  }

  const { worker } = await import('./browser');

  // Start the worker and log status
  return worker.start({
    onUnhandledRequest: 'bypass', // Don't warn about non-API requests
    quiet: false, // Show MSW logs in console
  });
}
