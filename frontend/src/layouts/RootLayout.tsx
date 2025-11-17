import { useState } from "react";
import { Outlet } from "react-router-dom";
import { UploadSidebar } from "@/components/upload";
import { Header } from "@/components/common";

/**
 * RootLayout component provides the main application layout
 *
 * Includes:
 * - Top bar with upload button
 * - Floating upload sidebar (opened via button)
 * - Suspense boundary for lazy-loaded routes
 * - Main content area with Outlet for child routes
 */
export default function RootLayout() {
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Top Bar with Upload Button */}
      <Header onUploadClick={() => setIsUploadOpen(true)} />

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {/* Temporarily removed Suspense to debug remounting issue */}
        <Outlet />
      </main>

      {/* Floating Upload Sidebar */}
      <UploadSidebar
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
      />
    </div>
  );
}
