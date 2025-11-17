/**
 * Minimalistic mock server for testing frontend without real backend
 *
 * Simulates all three API endpoints:
 * - POST /api/upload
 * - GET /api/status/:jobId
 * - GET /api/employees
 *
 * Usage: Import and call setupMockServer() before rendering the app
 */

import { createMockJob, getMockJobStatus, filterEmployees } from './mockData';
import type { UploadResponse } from '@/types/job.types';
import type { EmployeesResponse } from '@/types/employee.types';

interface MockRequest {
  method: string;
  url: string;
  body?: unknown;
  params?: Record<string, string>;
  query?: Record<string, string>;
}

interface MockResponse {
  status: number;
  data?: unknown;
  error?: string;
}

/**
 * Parse URL to extract path, params, and query
 */
function parseUrl(url: string): { path: string; params: Record<string, string>; query: Record<string, string> } {
  const [pathAndQuery] = url.split('?');
  const queryString = url.includes('?') ? url.split('?')[1] : '';

  const query: Record<string, string> = {};
  if (queryString) {
    queryString.split('&').forEach(param => {
      const [key, value] = param.split('=');
      if (key && value !== undefined) {
        query[decodeURIComponent(key)] = decodeURIComponent(value);
      }
    });
  }

  return {
    path: pathAndQuery,
    params: {},
    query,
  };
}

/**
 * Mock server request handler
 */
function handleMockRequest(request: MockRequest): MockResponse {
  const { method, url } = request;
  const { path, query } = parseUrl(url);

  console.log(`[MOCK SERVER] ${method} ${url}`);

  // POST /api/upload
  if (method === 'POST' && path === '/api/upload') {
    const filename = (request.body as { filename?: string })?.filename || 'input.xlsx';
    const fileSize = 245760; // Default file size
    const job_id = createMockJob(filename, fileSize);

    const response: UploadResponse = { job_id };
    return { status: 200, data: response };
  }

  // GET /api/status/:jobId
  if (method === 'GET' && path.startsWith('/api/status/')) {
    const job_id = path.split('/api/status/')[1];
    const jobStatus = getMockJobStatus(job_id);

    if (!jobStatus) {
      return { status: 404, error: 'Job not found' };
    }

    return { status: 200, data: jobStatus };
  }

  // GET /api/employees
  if (method === 'GET' && path === '/api/employees') {
    const params = {
      page: query.page ? parseInt(query.page) : 1,
      page_size: query.page_size ? parseInt(query.page_size) : 20,
      sort_by: query.sort_by,
      order: query.order as 'asc' | 'desc' | undefined,
      search: query.search,
      department: query.department,
    };

    const response: EmployeesResponse = filterEmployees(params);
    return { status: 200, data: response };
  }

  // 404 for unknown routes
  return { status: 404, error: `Not found: ${method} ${path}` };
}

/**
 * Intercept axios requests and return mock responses
 */
export function setupMockServer() {
  // This is a simplified version - in production you'd use MSW (Mock Service Worker)
  // or axios-mock-adapter for better interception

  console.log('[MOCK SERVER] Mock server enabled - all API requests will use mock data');
  console.log('[MOCK SERVER] Available endpoints:');
  console.log('[MOCK SERVER]   POST /api/upload');
  console.log('[MOCK SERVER]   GET  /api/status/:jobId');
  console.log('[MOCK SERVER]   GET  /api/employees');

  return {
    handleRequest: handleMockRequest,
  };
}

/**
 * Axios interceptor setup for mock server
 *
 * Call this BEFORE creating axios instance to intercept all requests
 */
export function setupMockAxiosInterceptor() {
  // Note: This requires axios-mock-adapter or MSW for proper implementation
  // For now, this is just a placeholder showing the structure
  console.warn('[MOCK SERVER] To use mock server, install axios-mock-adapter or MSW');
  console.warn('[MOCK SERVER] npm install axios-mock-adapter --save-dev');
}

// Export mock functions for direct testing
export { createMockJob, getMockJobStatus, filterEmployees };
