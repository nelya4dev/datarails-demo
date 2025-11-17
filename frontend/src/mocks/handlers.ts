/**
 * MSW request handlers for mock API
 *
 * Defines all API endpoint mocks using Mock Service Worker
 */

import { http, HttpResponse, delay } from 'msw';
import { createMockJob, getMockJobStatus, filterEmployees, getJobsList } from './mockData';
import type { UploadResponse } from '@/types/job.types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const handlers = [
  // POST /api/upload - File upload
  http.post(`${API_BASE_URL}/api/upload`, async ({ request }) => {
    await delay(800); // Simulate network delay

    try {
      const formData = await request.formData();
      const file = formData.get('file') as File;

      if (!file) {
        return HttpResponse.json(
          { detail: 'No file provided' },
          { status: 400 }
        );
      }

      // Validate file type
      if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
        return HttpResponse.json(
          { detail: 'Only .xlsx and .xls files are supported' },
          { status: 400 }
        );
      }

      // Validate file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        return HttpResponse.json(
          { detail: 'File size must be less than 10MB' },
          { status: 413 }
        );
      }

      const job_id = createMockJob(file.name, file.size);
      const response: UploadResponse = { job_id };

      console.log(`[MOCK] File uploaded: ${file.name} → job_id: ${job_id}`);

      return HttpResponse.json(response, { status: 200 });
    } catch (error) {
      return HttpResponse.json(
        { detail: 'Upload failed' },
        { status: 500 }
      );
    }
  }),

  // GET /api/status/:jobId - Job status
  http.get(`${API_BASE_URL}/api/status/:jobId`, async ({ params }) => {
    await delay(100); // Simulate network delay

    const { jobId } = params;
    const jobStatus = getMockJobStatus(jobId as string);

    if (!jobStatus) {
      return HttpResponse.json(
        { detail: 'Job not found' },
        { status: 404 }
      );
    }

    console.log(`[MOCK] Job status: ${jobId} → ${jobStatus.status} (${jobStatus.current_step})`);

    return HttpResponse.json(jobStatus, { status: 200 });
  }),

  // GET /api/employees - Employees list with filters
  http.get(`${API_BASE_URL}/api/employees`, async ({ request }) => {
    await delay(200); // Simulate network delay

    const url = new URL(request.url);
    const params = {
      page: url.searchParams.get('page') ? parseInt(url.searchParams.get('page')!) : 1,
      page_size: url.searchParams.get('page_size') ? parseInt(url.searchParams.get('page_size')!) : 20,
      sort_by: url.searchParams.get('sort_by') || undefined,
      order: (url.searchParams.get('order') as 'asc' | 'desc') || undefined,
      search: url.searchParams.get('search') || undefined,
      department: url.searchParams.get('department') || undefined,
    };

    const response = filterEmployees(params);

    console.log(
      `[MOCK] Employees: page=${params.page}, size=${params.page_size}, ` +
      `search=${params.search || 'none'}, dept=${params.department || 'all'} ` +
      `→ ${response.employees.length} results`
    );

    return HttpResponse.json(response, { status: 200 });
  }),

  // GET /api/jobs - Jobs list with filters
  http.get(`${API_BASE_URL}/api/jobs`, async ({ request }) => {
    await delay(150); // Simulate network delay

    const url = new URL(request.url);
    const params = {
      page: url.searchParams.get('page') ? parseInt(url.searchParams.get('page')!) : 1,
      page_size: url.searchParams.get('page_size') ? parseInt(url.searchParams.get('page_size')!) : 20,
      status: url.searchParams.get('status') as 'pending' | 'processing' | 'completed' | 'failed' | undefined,
      sort_by: url.searchParams.get('sort_by') || undefined,
      order: (url.searchParams.get('order') as 'asc' | 'desc') || undefined,
    };

    const response = getJobsList(params);

    console.log(
      `[MOCK] Jobs: page=${params.page}, size=${params.page_size}, ` +
      `status=${params.status || 'all'} → ${response.jobs.length} results`
    );

    return HttpResponse.json(response, { status: 200 });
  }),
];
