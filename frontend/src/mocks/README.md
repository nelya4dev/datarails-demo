# Mock Server

Mock API server using [MSW (Mock Service Worker)](https://mswjs.io/) for frontend development and testing without a real backend.

## Features

- ✅ **Realistic data** - Based on actual `input.xlsx` file structure
- ✅ **500 mock employees** - Full dataset for testing pagination, search, filters
- ✅ **Job processing simulation** - Simulates async job lifecycle (pending → processing → completed)
- ✅ **Error handling** - Includes validation errors from real Excel data issues
- ✅ **Network delays** - Realistic API response times (100-800ms)
- ✅ **Type-safe** - Uses existing TypeScript types

## Usage

### Enable Mock Server

Set environment variable in `.env`:

```env
VITE_USE_MOCKS=true
```

### Disable Mock Server

Use real backend API:

```env
VITE_USE_MOCKS=false
# or simply remove the variable
```

### Test with Mock Data

1. **Upload File**: Drag any .xlsx file → mock server creates job
2. **Job Status**: Auto-polling shows progression through 6 steps
3. **Employees List**: Browse 500 mock employees with search/filters

## Mock Data

### Employees

- **Count**: 500 records
- **Departments**: Development, Finance, Marketing, HR, R&D, Operations
- **Salary Range**: €35,000 - €100,000
- **Tenure**: Calculated based on hire dates (2015-2024)
- **Names**: 50 realistic names from actual Excel file

### Job Errors

Based on real data quality issues found in `input.xlsx`:

```typescript
[
  { row: 15, field: 'salary', message: 'Invalid numeric value' },
  { row: 142, field: 'department_code', message: 'Invalid code: "fin"' },
  { row: 156, field: 'employee_id', message: 'Missing required field' },
  { row: 259, field: 'name', message: 'Extra whitespace' },
  // ... 8 total errors
]
```

### Job Processing

Simulated timeline (~12 seconds):

```
0s   → pending
1s   → processing (reading)
3s   → processing (validating)
6s   → processing (transforming)
10s  → processing (persisting)
12s  → completed
```

## API Endpoints

All standard endpoints are mocked:

### POST /api/upload

```bash
# Request
POST /api/upload
Content-Type: multipart/form-data
file: <File>

# Response
{ "job_id": "550e8400-e29b-41d4-a716-446655440000" }
```

**Validation**:
- File type: `.xlsx` or `.xls`
- Max size: 10MB
- Returns 400/413 for invalid uploads

### GET /api/status/:jobId

```bash
# Request
GET /api/status/550e8400-e29b-41d4-a716-446655440000

# Response
{
  "job_id": "...",
  "filename": "input.xlsx",
  "status": "processing",
  "current_step": "validating",
  "total_rows": 508,
  "processed_rows": 245,
  "error_rows": 8,
  "errors": [...],
  "started_at": "2025-11-16T14:32:15Z",
  "completed_at": null
}
```

**Job lifecycle**: Auto-progresses through statuses

### GET /api/employees

```bash
# Request
GET /api/employees?page=1&page_size=20&search=john&department=Development&sort_by=name&order=asc

# Response
{
  "employees": [...],
  "total": 500,
  "page": 1,
  "page_size": 20,
  "total_pages": 25
}
```

**Features**:
- Pagination (default 20 per page)
- Search by name/ID
- Filter by department
- Sort by any column (asc/desc)

## Files

```
src/mocks/
├── README.md          # This file
├── index.ts           # Entry point (conditional enable)
├── browser.ts         # MSW browser setup
├── handlers.ts        # API endpoint handlers
├── mockData.ts        # Data generators & storage
└── server.ts          # Standalone server (legacy, unused)
```

## Development

### Add New Endpoint

1. Edit `handlers.ts`:

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  // ... existing handlers

  http.get('/api/new-endpoint', async () => {
    return HttpResponse.json({ data: 'mock response' });
  }),
];
```

2. Mock data automatically used

### Modify Mock Data

Edit `mockData.ts`:

```typescript
// Add more employees
export const MOCK_EMPLOYEES = generateEmployees(1000);

// Add more errors
export const MOCK_JOB_ERRORS = [
  // ... add new error objects
];
```

## Console Logs

When mock server is active, you'll see:

```
[MSW] Mocking enabled.
[MOCK] File uploaded: input.xlsx → job_id: abc-123
[MOCK] Job status: abc-123 → processing (validating)
[MOCK] Employees: page=1, size=20, search=none, dept=all → 20 results
```

## Performance

- **Network delays**: 100-800ms (realistic)
- **Job processing**: 12s total (simulated async)
- **No backend required**: Works offline
- **Fast iteration**: Instant changes, no API deploy

## Switching to Real Backend

1. Set `VITE_USE_MOCKS=false` in `.env`
2. Point `VITE_API_BASE_URL` to real backend
3. No code changes needed - same API contract

## Notes

- Mock server only runs in browser (not in Node/tests)
- Uses Service Worker (registered at `/mockServiceWorker.js`)
- Gracefully bypasses non-API requests
- Can be toggled via environment variable
