import { FileSpreadsheet, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { formatFileSize } from '@/utils/validators';

interface FilePreviewProps {
  file: File;
  onRemove: () => void;
}

/**
 * FilePreview component displays selected file information
 *
 * Shows file name, size, and provides option to remove file.
 *
 * @example
 * ```tsx
 * <FilePreview
 *   file={selectedFile}
 *   onRemove={() => setSelectedFile(null)}
 * />
 * ```
 */
export function FilePreview({ file, onRemove }: FilePreviewProps) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          <div className="rounded-lg bg-primary/10 p-3">
            <FileSpreadsheet className="h-8 w-8 text-primary" />
          </div>

          <div className="flex-1 min-w-0">
            <p className="font-medium truncate" title={file.name}>
              {file.name}
            </p>
            <p className="text-sm text-muted-foreground">
              {formatFileSize(file.size)}
            </p>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onRemove}
            aria-label="Remove file"
            className="hover:bg-destructive/10 hover:text-destructive"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
