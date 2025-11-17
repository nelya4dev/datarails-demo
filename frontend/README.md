# 🎨 Frontend - Data Ingestion Service

A React-based web application for uploading Excel files, monitoring processing jobs in real-time, and viewing transformed employee data.

## 🏗️ Architecture Overview

**Important:** Employees are stored in a **shared table** (not job-specific). The backend merges employee data from all uploads using UPSERT on `employee_id`. Jobs track metadata only (filename, status, error count), not which specific employees came from each job. The Employees page shows all employees from all uploads combined.

## 📋 Features

- **File Upload**: Drag & drop Excel files (.xlsx, .xls) with validation
- **Real-time Status Tracking**: Monitor job progress with auto-refresh polling
- **Data Visualization**: Searchable, filterable, sortable employee data table
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS

## 🛠️ Tech Stack

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: TanStack Query v5 (server state with retry logic)
- **HTTP Client**: Axios
- **UI Framework**: Tailwind CSS 3
- **Component Library**: shadcn/ui
- **File Upload**: react-dropzone
- **Data Tables**: TanStack Table v8
- **Date Formatting**: date-fns
- **Icons**: Lucide React

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MAX_FILE_SIZE_MB=10
VITE_POLLING_INTERVAL_MS=2000
```

## 📁 Project Structure

```
src/
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── upload/           # File upload components
│   ├── status/           # Job status components
│   ├── employees/        # Employee list components
│   └── common/           # Shared components (Header, etc.)
├── pages/                # Route pages
├── services/             # API layer (Axios)
├── hooks/                # Custom React hooks
├── types/                # TypeScript type definitions
├── utils/                # Utility functions
└── lib/                  # Utilities (cn helper, etc.)
```

## 🚀 Pages & Routes

- `/` - Jobs list (view all upload jobs with status)
- `/jobs/:jobId` - Job status page (track processing progress and errors)
- `/employees` - All employees (view all employees from shared table)
- `*` - 404 Not Found

**Navigation:** Header includes links to Jobs and Employees pages with active state highlighting.

## 🎨 UI Components (shadcn/ui)

Installed components:

- Button
- Card
- Input
- Table
- Progress
- Alert
- Badge
- Select
- Dropdown Menu

To add more components:

```bash
npx shadcn@latest add [component-name]
```

## 📡 API Integration

The frontend expects the following API endpoints:

### POST /api/upload

Upload Excel file and get job ID

**Request**: `multipart/form-data` with file
**Response**: `{ job_id: string }`

### GET /api/status/:jobId

Get job processing status

**Response**:

```json
{
  "job_id": "uuid",
  "filename": "input.xlsx",
  "status": "processing",
  "current_step": "validating",
  "total_rows": 1000,
  "processed_rows": 450,
  "error_rows": 12,
  "errors": [...],
  "started_at": "2025-11-16T14:32:15Z",
  "completed_at": null
}
```

### GET /api/employees

Get all employees from shared table (merged from all uploads)

**Query Params**: `page`, `page_size`, `sort_by`, `order`, `search`, `department`

**Response**:

```json
{
  "employees": [
    {
      "id": "uuid",
      "created_at": "2025-11-17T10:00:00Z",
      "updated_at": "2025-11-17T10:00:00Z",
      "employee_id": "E0001",
      "name": "John Doe",
      "department_code": "DEV",
      "salary": 75000.0,
      "hire_date": "2023-01-15",
      "department_name": "Development",
      "annual_salary_eur": 69000.0,
      "tenure_years": 2
    }
  ],
  "total": 1234,
  "page": 1,
  "page_size": 20,
  "total_pages": 62
}
```

**Note:** This endpoint returns ALL employees (not job-specific). Backend uses UPSERT on `employee_id` to merge data from multiple uploads.

## 🔄 State Management

- **Server State**: TanStack Query with automatic retry and caching
- **UI State**: React useState hooks
- **Auto-refresh**: Job status polling every 2 seconds while processing

## 🎯 Development Guidelines

### Code Standards

- **TypeScript**: Strict mode enabled
- **Components**: Functional components with hooks
- **Styling**: Tailwind utility classes
- **Naming**: PascalCase for components, camelCase for functions

### Adding shadcn Components

```bash
# List available components
npx shadcn@latest add

# Add specific component
npx shadcn@latest add dialog
```

### Path Aliases

Use `@/` prefix for imports:

```typescript
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
```

## 📚 Documentation

Comprehensive documentation is available in the [docs/](./docs) directory:

- [docs/PRD.md](./docs/PRD.md) - Product Requirements Document
- [docs/ROADMAP.md](./docs/ROADMAP.md) - Implementation Roadmap
- [docs/ASSIGNMENT.md](./docs/ASSIGNMENT.md) - Original Assignment
- [docs/README.md](./docs/README.md) - Full documentation index

## 🧪 Testing

Testing is optional for this MVP. If implementing tests:

```bash
# Unit tests (if implemented)
npm run test

# E2E tests (not in scope)
npm run test:e2e
```

## 🚢 Deployment

### Build

```bash
npm run build
# Output: dist/
```

### Docker (Optional)

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Hosting Options

- **Vercel**: Connect GitHub repo for automatic deployments
- **Netlify**: Drag & drop `dist/` folder
- **AWS S3 + CloudFront**: Static hosting

## 📝 License

This project is for assignment purposes.

## 🤝 Contributing

This is an assignment project. See [docs/ASSIGNMENT.md](./docs/ASSIGNMENT.md) for requirements.
