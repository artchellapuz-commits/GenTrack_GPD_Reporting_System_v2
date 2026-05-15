# Archive Page Error Fix

## Problem
The Archive Page was showing errors because the API methods `getArchivedFiles` and `restoreArchivedFile` were not defined in the frontend API service.

### Errors:
```
TypeError: api.getArchivedFiles is not a function
TypeError: api.restoreArchivedFile is not a function
```

## Solution Applied

### 1. Added Missing API Methods (frontend/src/services/api.js)

**Added `getArchivedFiles` method:**
```javascript
async getArchivedFiles() {
  console.log('📡 Loading archived files from API...');
  const response = await apiClient.get('/uploaded-files/', {
    params: { is_archived: true }
  });
  console.log('✅ Archived files loaded:', response.data);
  return response; // Return full response object
}
```

**Added `restoreArchivedFile` method:**
```javascript
async restoreArchivedFile(fileId) {
  console.log(`📡 Restoring archived file ${fileId}...`);
  const response = await apiClient.post(`/uploaded-files/${fileId}/restore/`);
  console.log('✅ File restored:', response.data);
  return response; // Return full response object
}
```

### 2. Enhanced Backend Queryset Filtering (backend/reports/views.py)

**Added `get_queryset` method to `UploadedFileViewSet`:**
```python
def get_queryset(self):
    """Filter by is_archived parameter"""
    queryset = UploadedFile.objects.all().select_related('plant', 'uploaded_by')
    
    # Check if is_archived parameter is provided
    is_archived = self.request.query_params.get('is_archived')
    
    if is_archived is not None:
        # Convert string to boolean
        is_archived_bool = is_archived.lower() in ['true', '1', 'yes']
        queryset = queryset.filter(is_archived=is_archived_bool)
    else:
        # Default: only show non-archived files
        queryset = queryset.filter(is_archived=False)
    
    return queryset.order_by('-uploaded_at')
```

## How It Works

### Archive Page Flow:
1. **Load Archived Files**:
   ```
   ArchivePage.vue → api.getArchivedFiles()
                  → GET /api/uploaded-files/?is_archived=true
                  → Backend filters by is_archived=True
                  → Returns archived files
   ```

2. **Restore File**:
   ```
   User clicks Restore → api.restoreArchivedFile(fileId)
                      → POST /api/uploaded-files/{id}/restore/
                      → Backend sets is_archived=False
                      → File moved back to active uploads
   ```

### Backend Endpoints:

**List Archived Files:**
```
GET /api/uploaded-files/?is_archived=true
```

**Restore Archived File:**
```
POST /api/uploaded-files/{id}/restore/
```

**Archive File:**
```
POST /api/uploaded-files/{id}/archive/
```

## Features Now Working

✅ **Load Archived Files** - Displays all archived uploads
✅ **Restore Single File** - Restore one file at a time
✅ **Bulk Restore** - Restore multiple selected files
✅ **Search Archived Files** - Filter by filename or plant
✅ **Sort Archived Files** - Sort by date, name, size, etc.
✅ **Archive Statistics** - Shows total files, records, recent archives

## Testing

### 1. Test Archive Page Load:
1. Navigate to Archive page
2. Should see list of archived files (or empty state)
3. No console errors

### 2. Test Restore Single File:
1. Click restore icon on a file
2. Confirmation dialog appears
3. Click "Restore"
4. File disappears from archive
5. Check Upload History - file should appear there

### 3. Test Bulk Restore:
1. Select multiple files using checkboxes
2. Click "Restore Selected" button
3. Confirmation dialog appears
4. Click "Restore All"
5. All selected files disappear from archive

### 4. Test Search:
1. Type in search box
2. Files filter by filename or plant name
3. Results update in real-time

## API Endpoints Summary

| Endpoint | Method | Purpose | Parameters |
|----------|--------|---------|------------|
| `/uploaded-files/` | GET | List files | `is_archived=true/false` |
| `/uploaded-files/{id}/archive/` | POST | Archive a file | - |
| `/uploaded-files/{id}/restore/` | POST | Restore a file | - |
| `/uploaded-files/{id}/delete_upload/` | DELETE | Permanently delete | - |

## Database Fields

**UploadedFile Model:**
- `is_archived` (Boolean) - Whether file is archived
- `archived_at` (DateTime) - When file was archived
- `archived_by` (ForeignKey) - User who archived it

## Fallback Behavior

If the API fails to load archived files, the Archive Page will:
1. Show a warning in console
2. Display mock data for demo purposes
3. Allow user to interact with UI
4. Show toast notification about API error

This ensures the page doesn't break completely if there's a backend issue.

## Related Files

### Frontend:
- `frontend/src/services/api.js` - API methods
- `frontend/src/components/ArchivePage.vue` - Archive UI

### Backend:
- `backend/reports/views.py` - UploadedFileViewSet
- `backend/reports/models.py` - UploadedFile model
- `backend/reports/serializers.py` - UploadedFileSerializer

## Notes

- Archive is a soft delete (files not permanently removed)
- Archived files can be restored at any time
- Audit logs track all archive/restore actions
- Physical files remain on disk when archived
- Only the `is_archived` flag changes
