# Archive Page 404 Error Fix

## Problem
The Archive Page was showing a 404 error when trying to restore files:
```
POST http://localhost:8000/api/uploaded-files/1009/restore/ 404 (Not Found)
```

## Root Cause Analysis

### Issue 1: Mock Data with Non-Existent IDs
The Archive Page was generating **mock data** with IDs like 1009, 1010, etc., but these files don't actually exist in the database.

**Database Reality:**
- Only 7 uploaded files exist (IDs 1-7)
- None of them are archived
- File ID 1009 doesn't exist

**What Was Happening:**
1. Archive Page loads → No real archived files found
2. Falls back to mock data → Generates 45 fake files with IDs 1000-1044
3. User clicks restore on mock file → Tries to restore ID 1009
4. Backend can't find file → Returns 404 error

### Issue 2: Queryset Filtering
The `get_queryset()` method was filtering files, which could prevent the restore action from accessing archived files.

## Solutions Applied

### 1. Removed Mock Data Fallback (frontend/src/components/ArchivePage.vue)

**Before:**
```javascript
if (data.length === 0) {
  console.warn('No archived files found, using mock data for demo');
  archivedFiles.value = generateMockData();
}
```

**After:**
```javascript
if (data.length === 0) {
  console.log('No archived files found');
}
// Shows proper empty state instead of fake data
```

**Benefits:**
- ✅ No more fake files that can't be restored
- ✅ Shows real empty state when no archives exist
- ✅ Users see actual data only
- ✅ No confusing 404 errors

### 2. Added `get_object()` Override (backend/reports/views.py)

**Added method to bypass queryset filters:**
```python
def get_object(self):
    """Override to bypass queryset filters for detail actions"""
    # For archive and restore actions, get the object directly
    if self.action in ['archive', 'restore', 'delete_upload']:
        pk = self.kwargs.get('pk')
        try:
            return UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('File not found')
    
    # For other actions, use the default behavior
    return super().get_object()
```

**Benefits:**
- ✅ Archive/restore actions can access any file regardless of filters
- ✅ Prevents queryset from blocking access to archived files
- ✅ Proper 404 handling with clear error message

### 3. Added Explicit URL Paths

**Updated action decorators:**
```python
@action(detail=True, methods=['post'], url_path='archive')
def archive(self, request, pk=None):
    ...

@action(detail=True, methods=['post'], url_path='restore')
def restore(self, request, pk=None):
    ...
```

**Benefits:**
- ✅ Explicit URL routing
- ✅ Clearer endpoint structure
- ✅ Better debugging

## How Archive Works Now

### Archiving a File:
1. User uploads file → Appears in Upload History
2. User clicks Archive → File marked as archived
3. File disappears from Upload History
4. File appears in Archive Page

### Restoring a File:
1. User goes to Archive Page → Sees real archived files
2. User clicks Restore → File marked as not archived
3. File disappears from Archive Page
4. File reappears in Upload History

### Empty State:
1. No archived files → Shows empty state message
2. No fake data → No confusing errors
3. Clear call-to-action → "Archive files to see them here"

## Testing the Fix

### 1. Test Empty Archive:
```bash
# Check database
cd backend
python manage.py shell -c "from reports.models import UploadedFile; print(f'Archived: {UploadedFile.objects.filter(is_archived=True).count()}')"
```

Expected: `Archived: 0`

### 2. Test Archive Flow:
1. Go to Upload History
2. Click Archive on a file
3. File should disappear
4. Go to Archive Page
5. File should appear there
6. Click Restore
7. File should disappear from Archive
8. Go back to Upload History
9. File should reappear

### 3. Test Empty State:
1. Go to Archive Page with no archived files
2. Should see empty state message
3. No errors in console
4. No fake files displayed

## API Endpoints

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/uploaded-files/?is_archived=true` | GET | List archived files | ✅ Working |
| `/uploaded-files/{id}/archive/` | POST | Archive a file | ✅ Working |
| `/uploaded-files/{id}/restore/` | POST | Restore a file | ✅ Fixed |
| `/uploaded-files/{id}/delete_upload/` | DELETE | Delete permanently | ✅ Working |

## Database State

**Current State:**
- 7 uploaded files (IDs 1-7)
- 0 archived files
- 10 generation reports

**To Create Test Data:**
```python
# In Django shell
from reports.models import UploadedFile
from django.utils import timezone

# Archive a file
file = UploadedFile.objects.first()
file.is_archived = True
file.archived_at = timezone.now()
file.save()
```

## Key Changes Summary

### Frontend (ArchivePage.vue):
- ❌ Removed mock data generation
- ✅ Shows real empty state
- ✅ Better error handling
- ✅ No fake file IDs

### Backend (views.py):
- ✅ Added `get_object()` override
- ✅ Explicit URL paths for actions
- ✅ Bypasses queryset filters for restore
- ✅ Proper 404 error handling

## Benefits

1. **No More 404 Errors**: Only real files can be restored
2. **Better UX**: Clear empty state instead of fake data
3. **Data Integrity**: Users only see real archived files
4. **Debugging**: Easier to troubleshoot with real data
5. **Trust**: Users trust the system when it shows real data

## Related Files

- `frontend/src/components/ArchivePage.vue` - Archive UI
- `frontend/src/services/api.js` - API methods
- `backend/reports/views.py` - UploadedFileViewSet
- `backend/reports/models.py` - UploadedFile model

## Notes

- Archive is a soft delete (files not permanently removed)
- Physical files remain on disk when archived
- Only the `is_archived` flag changes
- Audit logs track all archive/restore actions
- Empty state encourages users to archive files
