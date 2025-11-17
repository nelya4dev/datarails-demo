import { useQuery } from '@tanstack/react-query';
import { getEmployees } from '@/services/endpoints';
import { shouldRetry, getRetryDelay } from '@/utils/retryConfig';
import type { EmployeeQueryParams } from '@/types/employee.types';

/**
 * Custom hook for fetching paginated employees list
 *
 * Supports pagination, search, filtering, and sorting.
 * Query key includes all params to create separate cache entries per configuration.
 * Uses smart retry logic - only retries on network/server errors.
 *
 * @param params - Query parameters for filtering, pagination, and sorting
 * @returns TanStack Query result with employees data
 *
 * @example
 * ```tsx
 * function EmployeesPage() {
 *   const [search, setSearch] = useState('');
 *   const [page, setPage] = useState(1);
 *
 *   const { data, isLoading, error } = useEmployees({
 *     page,
 *     page_size: 20,
 *     search,
 *     sort_by: 'name',
 *     order: 'asc',
 *   });
 *
 *   if (isLoading) return <LoadingSpinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *   if (!data || data.employees.length === 0) return <EmptyState />;
 *
 *   return (
 *     <>
 *       <SearchBar value={search} onChange={setSearch} />
 *       <EmployeesTable data={data.employees} />
 *       <Pagination
 *         currentPage={page}
 *         totalPages={data.total_pages}
 *         onPageChange={setPage}
 *       />
 *     </>
 *   );
 * }
 * ```
 */
export function useEmployees(params: EmployeeQueryParams) {
  return useQuery({
    queryKey: ['employees', params], // Params in key = separate cache per config
    queryFn: () => getEmployees(params),
    retry: shouldRetry,
    retryDelay: getRetryDelay,
    staleTime: 1000 * 60, // 1 minute - employee data doesn't change frequently
    placeholderData: (previousData) => previousData, // Keep previous data while fetching
  });
}
