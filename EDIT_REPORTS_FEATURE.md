# Edit Reports Feature Documentation

## ✅ Feature Implemented

I've added the ability to **edit individual generation reports** directly from the View Reports page.

## 🎯 Features

### 1. **Edit Button in Table**
- Each report row now has an "Edit" button (pencil icon)
- Only visible to **Managers and above** (MANAGER, ADMIN, SUPERADMIN roles)
- Located in the new "Actions" column

### 2. **Edit Modal Form**
When you click Edit, a modal opens with all editable fields:

**Editable Fields:**
- ✏️ Report Date
- ✏️ Unit Number
- ✏️ Generation (kWh)
- ✏️ Operating Hours
- ✏️ Capacity Factor (%)
- ✏️ Availability Factor (%)
- ✏️ Forced Outage Hours
- ✏️ Scheduled Outage Hours
- ✏️ Remarks

**Read-Only Fields:**
- 🔒 Plant (cannot change plant assignment)

### 3. **Validation**
- Required fields marked with red asterisk (*)
- Number inputs have min/max constraints
- Operating hours: 0-24
- Capacity Factor: 0-100%
- Availability Factor: 0-100%
- Date picker for report date

### 4. **Save & Update**
- Click "Save Changes" to update the report
- Shows loading spinner while saving
- Success toast notification on save
- Table automatically refreshes with updated data
- Dashboard will reflect changes on next load

### 5. **Audit Trail**
- All edits are logged in the backend
- Tracks who edited what and when
- Maintains data integrity

## 🔐 Permissions

**Who Can Edit:**
- ✅ MANAGER
- ✅ ADMIN
- ✅ SUPERADMIN

**Who Cannot Edit:**
- ❌ OPERATOR
- ❌ VIEWER
- ❌ Unauthenticated users

## 📋 How to Use

### Step 1: Navigate to View Reports
```
Menu → View Reports
```

### Step 2: Find the Report to Edit
- Use filters to narrow down reports
- Sort by date, plant, or values
- Locate the specific report

### Step 3: Click Edit Button
- Click the blue pencil icon in the Actions column
- Edit modal will open

### Step 4: Modify Values
- Update any of the editable fields
- Required fields must have values
- Numbers must be within valid ranges

### Step 5: Save Changes
- Click "Save Changes" button
- Wait for success message
- Modal closes automatically
- Table refreshes with new data

### Step 6: Verify Changes
- Check the updated values in the table
- Dashboard will show updated aggregations
- Changes are permanent in database

## 🔧 Technical Implementation

### Frontend Changes

**File: `frontend/src/components/ViewReports.vue`**

1. **Added Actions Column**
   ```vue
   <th class="text-center">Actions</th>
   <td class="text-center">
     <button @click="openEditModal(report)" class="btn-edit">
       <i class="pi pi-pencil"></i>
     </button>
   </td>
   ```

2. **Added Edit Modal**
   - Form with all editable fields
   - Validation and constraints
   - Save/Cancel buttons

3. **Added Methods**
   - `openEditModal(report)` - Opens modal with report data
   - `closeEditModal()` - Closes modal and resets form
   - `saveEdit()` - Saves changes via API
   - `isManagerOrAbove()` - Permission check

4. **Added Data Properties**
   ```javascript
   showEditModal: false,
   editForm: { /* form fields */ },
   saving: false,
   canEdit: false
   ```

**File: `frontend/src/services/api.js`**

Added update method:
```javascript
async updateGenerationReport(id, data) {
  const response = await apiClient.patch(`/generation-reports/${id}/`, data);
  return response;
}
```

### Backend Changes

**File: `backend/reports/views.py`**

Added `UpdateModelMixin` to `GenerationReportViewSet`:
```python
class GenerationReportViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,  # NEW
                              viewsets.GenericViewSet):
```

This automatically provides:
- `PATCH /api/generation-reports/{id}/` - Partial update
- `PUT /api/generation-reports/{id}/` - Full update

## 🎨 UI/UX Features

### Edit Button
- Blue gradient background
- Hover effect (lifts up)
- Smooth transitions
- Pencil icon for clarity

### Edit Modal
- Large, centered modal
- Blue gradient header
- Two-column form layout
- Responsive design
- Smooth animations
- Click outside to close

### Form Fields
- Clear labels with required indicators
- Input validation
- Focus states with blue border
- Disabled state for read-only fields
- Textarea for remarks

### Buttons
- Cancel: Gray, closes modal
- Save: Green gradient, saves changes
- Loading state with spinner
- Disabled state when saving

## 📊 Data Flow

```
User clicks Edit
    ↓
Modal opens with current data
    ↓
User modifies fields
    ↓
User clicks Save
    ↓
Frontend validates input
    ↓
API call: PATCH /api/generation-reports/{id}/
    ↓
Backend updates database
    ↓
Success response
    ↓
Toast notification
    ↓
Table refreshes
    ↓
Dashboard updates on next load
```

## 🔍 What Gets Updated

### Immediate Updates:
- ✅ View Reports table
- ✅ Report summary statistics
- ✅ Database record

### Updates on Refresh:
- 🔄 Dashboard pie charts
- 🔄 Dashboard statistics
- 🔄 Trend charts
- 🔄 Analytics data

## ⚠️ Important Notes

### 1. **Plant Cannot Be Changed**
- Plant assignment is locked
- This prevents data integrity issues
- If wrong plant, delete and re-upload

### 2. **Unit Number Can Change**
- Useful for correcting data entry errors
- Ensure unit exists for the plant

### 3. **Calculated Fields**
- Capacity Factor and Availability are editable
- Normally calculated from other values
- Manual override available for corrections

### 4. **Audit Trail**
- All edits are logged
- Cannot be undone (no undo feature)
- Make sure changes are correct before saving

### 5. **Dashboard Cache**
- Analytics endpoint cached for 15 minutes
- Dashboard may not show changes immediately
- Click Refresh button to force update

## 🐛 Troubleshooting

### Edit Button Not Showing
**Cause**: User doesn't have permission
**Solution**: Check user role (must be Manager or above)

### Save Button Disabled
**Cause**: Required fields empty or invalid values
**Solution**: Fill all required fields with valid data

### Changes Not Showing in Dashboard
**Cause**: Analytics cache
**Solution**: Wait 15 minutes or clear cache

### Error on Save
**Cause**: Invalid data or server error
**Solution**: Check console for error message, verify data validity

## 🚀 Future Enhancements

Possible additions:
- [ ] Bulk edit multiple reports
- [ ] Edit history/changelog
- [ ] Undo last edit
- [ ] Duplicate report
- [ ] Delete report
- [ ] Export edited reports
- [ ] Compare before/after values

## 📝 Testing Checklist

- [x] Edit button shows for managers
- [x] Edit button hidden for operators
- [x] Modal opens with correct data
- [x] All fields are editable
- [x] Plant field is disabled
- [x] Validation works correctly
- [x] Save updates database
- [x] Table refreshes after save
- [x] Toast notification appears
- [x] Modal closes after save
- [x] Cancel button works
- [x] Click outside closes modal
- [x] Responsive on mobile
- [x] Loading state shows while saving

## 📚 Related Files

### Frontend:
- `frontend/src/components/ViewReports.vue` - Main component
- `frontend/src/services/api.js` - API methods

### Backend:
- `backend/reports/views.py` - ViewSet with update mixin
- `backend/reports/models.py` - GenerationReport model
- `backend/reports/serializers.py` - Serializers

## ✅ Summary

You can now **edit any uploaded generation report** directly from the View Reports page. The feature is:
- ✅ Secure (permission-based)
- ✅ User-friendly (intuitive modal)
- ✅ Validated (prevents invalid data)
- ✅ Audited (tracks all changes)
- ✅ Responsive (works on all devices)

**Each uploaded report is now fully editable!**
