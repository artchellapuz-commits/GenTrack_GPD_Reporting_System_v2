# Upload and Dashboard Data Display Fix

## Problem Identified

### Issue 1: 400 Bad Request on File Upload
The upload endpoint was returning a 400 Bad Request error because the `@action` decorator was missing the `url_path='upload'` parameter. This caused the endpoint to not be properly registered with the router.

**Error:**
```
POST http://localhost:8000/api/uploaded-files/upload/
400 (Bad Request)
```

### Issue 2: Dashboard Not Displaying Uploaded Data
The dashboard loads data from the `GenerationReport` table through the analytics comparison endpoint. When files are uploaded successfully, they should:
1. Create an `UploadedFile` record
2. Process the Excel file using `ExcelImporter`
3. Create `GenerationReport` records for each row
4. These records are then aggregated and displayed on the dashboard

## Fix Applied

### Backend Fix (backend/reports/views.py)

**Before:**
```python
@audit_action('FILE_UPLOAD', 'File upload and processing', category='file_management', severity='MEDIUM')
def upload(self, request):
```

**After:**
```python
@action(detail=False, methods=['post'], url_path='upload')
@audit_action('FILE_UPLOAD', 'File upload and processing', category='file_management', severity='MEDIUM')
def upload(self, request):
```

## How the Data Flow Works

### 1. File Upload Process
```
User uploads Excel → Frontend calls /api/uploaded-files/upload/
                  ↓
Backend receives file → Creates UploadedFile record
                  ↓
ExcelImporter processes file → Creates GenerationReport records
                  ↓
Returns success with records_imported count
```

### 2. Dashboard Data Loading
```
Dashboard loads → Calls /api/analytics/comparison/
                  ↓
Analytics service queries GenerationReport table
                  ↓
Aggregates data by plant (generation, capacity factor, availability)
                  ↓
Returns plant statistics to dashboard
                  ↓
Dashboard displays pie charts and tables
```

### 3. Data Aggregation
The analytics service (`backend/reports/services/analytics_service.py`) performs:
- `Sum(generation_kwh)` - Total generation per plant
- `Avg(capacity_factor)` - Average capacity factor
- `Avg(availability_factor)` - Average availability
- `Count(id)` - Number of reports (days_reported)

## Testing the Fix

### 1. Restart Backend Server
```bash
cd backend
python manage.py runserver
```

### 2. Test File Upload
1. Navigate to Upload Excel page
2. Select a plant from dropdown
3. Choose an Excel file with the correct format
4. Click Upload
5. Should see success message with "X records imported successfully"

### 3. Verify Dashboard Display
1. Navigate to Dashboard
2. Should see:
   - Plant Capacity pie chart with data
   - Generation Distribution pie chart with data
   - Plant Performance Summary table populated
   - Statistics cards showing totals

### 4. Check Console Logs
**Frontend (Browser Console):**
```
🔄 Loading dashboard data...
🔄 Loading plants stats from analytics endpoint...
📊 Analytics response: {plants: [...], fleet_summary: {...}}
✅ Processed plants data: [...]
```

**Backend (Terminal):**
```
File uploaded and processed successfully
X records imported from filename.xlsx
```

## Expected Excel File Format

The Excel file should contain columns matching the `GenerationReport` model:
- Date/Report Date
- Plant Code
- Unit Number
- Generation (kWh)
- Capacity Factor (%)
- Availability Factor (%)
- Operating Hours
- Forced Outage Hours
- etc.

## Troubleshooting

### If Upload Still Fails:
1. Check backend logs for specific error messages
2. Verify plant code exists in database
3. Check Excel file format matches expected columns
4. Ensure file is not a duplicate (checksum validation)

### If Dashboard Shows No Data:
1. Verify GenerationReport records were created:
   ```python
   python manage.py shell
   from reports.models import GenerationReport
   GenerationReport.objects.count()  # Should be > 0
   ```

2. Check analytics endpoint directly:
   ```
   GET http://localhost:8000/api/analytics/comparison/
   ```

3. Clear browser cache and refresh dashboard

### If Data Appears Incorrect:
1. Check date range filters
2. Verify plant codes match between upload and dashboard
3. Check for data validation errors in upload logs

## Related Files

### Backend:
- `backend/reports/views.py` - Upload endpoint
- `backend/reports/services/analytics_service.py` - Data aggregation
- `backend/reports/models.py` - Data models
- `backend/reports/importers/excel_importer.py` - Excel processing

### Frontend:
- `frontend/src/components/UploadExcel.vue` - Upload UI
- `frontend/src/components/Dashboard.vue` - Dashboard display
- `frontend/src/services/api.js` - API calls

## Additional Notes

- The upload endpoint now properly handles authentication and CSRF
- Duplicate file detection is based on SHA256 checksum
- Files are processed synchronously (may take time for large files)
- Dashboard data is cached for 15 minutes to improve performance
- All uploads are logged in the audit trail
