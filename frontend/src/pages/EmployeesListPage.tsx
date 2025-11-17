import { useState, useMemo } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { LoadingSpinner, ErrorAlert, EmptyState } from "@/components/common";
import { EmployeesTable, SearchBar, Pagination, DepartmentFilter } from "@/components/employees";
import { useEmployees } from "@/hooks";

function EmployeesListPage() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("all");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  // Memoize params to prevent creating new object on every render
  const queryParams = useMemo(
    () => ({
      page,
      page_size: pageSize,
      search: search || undefined,
      department: department !== "all" ? department : undefined,
      sort_by: "name" as const,
      order: "asc" as const,
    }),
    [page, pageSize, search, department]
  );

  const { data, isPending, isFetching, error } = useEmployees(queryParams);

  // Initial loading state (no data yet)
  if (isPending) {
    return (
      <div className="p-6">
        <Card>
          <CardContent className="py-12">
            <LoadingSpinner text="Loading employees..." />
          </CardContent>
        </Card>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="p-6">
        <ErrorAlert error={error as Error} title="Failed to load employees" />
      </div>
    );
  }

  // True empty state - no data at all (no uploads yet)
  const hasNoDataAtAll = !data || (data.total === 0 && !search && department === "all");
  const hasNoSearchResults = data && data.items.length === 0 && (search || department !== "all");

  return (
    <div className="p-6 space-y-4">
      {/* Search and Filter - Always visible */}
      <div className="flex items-center gap-4">
        <SearchBar
          value={search}
          onChange={(value) => {
            setSearch(value);
            setPage(1); // Reset to first page on search
          }}
          placeholder="Search by name, department, or employee ID"
        />
        <DepartmentFilter
          value={department}
          onChange={(value) => {
            setDepartment(value);
            setPage(1); // Reset to first page on filter change
          }}
        />
        {/* Background loading indicator */}
        {isFetching && (
          <span className="text-sm text-muted-foreground flex items-center gap-2">
            <LoadingSpinner />
          </span>
        )}
      </div>

      {/* Empty state when no uploads yet */}
      {hasNoDataAtAll ? (
        <Card>
          <CardContent className="py-12">
            <EmptyState
              title="No Employees Found"
              description="Upload a file to import employee data"
            />
          </CardContent>
        </Card>
      ) : hasNoSearchResults ? (
        /* No search results - show message in table */
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            No employees match &quot;{search}&quot;
          </CardContent>
        </Card>
      ) : (
        /* Table with data */
        <>
          <Card>
            <CardContent className="p-0">
              <div className={isFetching ? "opacity-60 pointer-events-none" : ""}>
                <EmployeesTable data={data?.items || []} />
              </div>
            </CardContent>
          </Card>

          {/* Pagination */}
          {data && data.pages > 1 && (
            <div className="flex justify-center">
              <Pagination
                currentPage={page}
                totalPages={data.pages}
                pageSize={pageSize}
                totalItems={data.total}
                onPageChange={setPage}
                onPageSizeChange={(newSize) => {
                  setPageSize(newSize);
                  setPage(1); // Reset to first page on page size change
                }}
              />
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default EmployeesListPage;
