import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Upload, Briefcase, Users } from "lucide-react";
import { cn } from "@/lib/utils";

interface HeaderProps {
  onUploadClick: () => void;
}

function Header({ onUploadClick }: HeaderProps) {
  const location = useLocation();

  return (
    <header className="border-b bg-background px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-8">
          <h1 className="text-xl font-semibold">Data Ingestion Service</h1>

          <nav className="flex items-center gap-4">
            <Link
              to="/"
              className={cn(
                "flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary",
                location.pathname === "/"
                  ? "text-foreground"
                  : "text-muted-foreground"
              )}
            >
              <Briefcase className="h-4 w-4" />
              Jobs
            </Link>
            <Link
              to="/employees"
              className={cn(
                "flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary",
                location.pathname === "/employees"
                  ? "text-foreground"
                  : "text-muted-foreground"
              )}
            >
              <Users className="h-4 w-4" />
              Employees
            </Link>
          </nav>
        </div>

        <Button onClick={onUploadClick} size="default">
          <Upload className="h-4 w-4 mr-2" />
          Upload .xls, .csv
        </Button>
      </div>
    </header>
  );
}

export default Header;
