import { lazy, Suspense, useMemo } from "react";
import type { LazyExoticComponent, ReactElement } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import RootLayout from "./layouts/RootLayout";
import { LoadingSpinner } from "./components/common";

// Lazy load route components for code splitting
const JobsListPage = lazy(() => import("./pages/JobsListPage"));
const JobStatusPage = lazy(() => import("./pages/JobStatusPage"));
const EmployeesListPage = lazy(() => import("./pages/EmployeesListPage"));
const NotFoundPage = lazy(() => import("./pages/NotFoundPage"));

// Wrapper component that provides Suspense boundary for lazy routes
function LazyRoute({
  Component,
}: {
  Component: LazyExoticComponent<() => ReactElement>;
}) {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner />
        </div>
      }
    >
      <Component />
    </Suspense>
  );
}

/**
 * Router component that provides routing context
 *
 * Uses React Router v6 with lazy loading for optimal performance.
 * Routes are split into separate chunks loaded on-demand.
 *
 * Router is memoized for Fast Refresh compatibility and performance.
 */
export function Router() {
  const router = useMemo(
    () =>
      createBrowserRouter([
        {
          path: "/",
          element: <RootLayout />,
          children: [
            {
              index: true,
              element: <LazyRoute Component={JobsListPage} />,
            },
            {
              path: "jobs/:jobId",
              element: <LazyRoute Component={JobStatusPage} />,
            },
            {
              path: "employees",
              element: <LazyRoute Component={EmployeesListPage} />,
            },
            {
              path: "*",
              element: <LazyRoute Component={NotFoundPage} />,
            },
          ],
        },
      ]),
    [] // Empty deps - router created once
  );

  return <RouterProvider router={router} />;
}
