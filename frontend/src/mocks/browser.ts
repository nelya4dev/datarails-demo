/**
 * MSW browser setup for development
 *
 * Starts the mock service worker in the browser to intercept API requests
 */

import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
