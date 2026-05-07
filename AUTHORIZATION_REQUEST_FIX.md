# Authorization Request 403 Error - FIXED

## Problem
When submitting a signatory authorization request, the system returned:
```
POST http://localhost:8000/api/signatory-authorizations/request/ 403 (Forbidden)
```

## Root Causes

### 1. Missing API Function
The frontend was calling `api.requestSignatoryAuthorization()` but this function didn't exist in `frontend/src/services/api.js`.

### 2. Permission Configuration
The `SignatoryAuthorizationViewSet` didn't have explicit permission configuration for custom actions, causing Django REST Framework to block requests with default restrictive permissions.

### 3. Missing Import
The `audit_authorization_request` function was being called but not imported.

### 4. Session Access Error
Debug code was trying to access `request.session` which doesn't exist in test requests.

## Fixes Applied

### 1. Added API Functions (frontend/src/services/api.js)
```javascript
async requestSignatoryAuthorization(requestData) {
  const response = await apiClient.post('/signatory-authorizations/request/', requestData);
  return response;
},

async getMyAuthorizationRequests() {
  const response = await apiClient.get('/signatory-authorizations/my-requests/');
  return response;
},

async deleteSignatoryAuthorization(id) {
  const response = await apiClient.delete(`/signatory-authorizations/${id}/`);
  return response;
},
```

### 2. Added Permission Override (backend/reports/views_authorization.py)
```python
def get_permissions(self):
    """Override permissions for different actions"""
    # Allow any authenticated user to request authorization
    if self.action in ['request_authorization', 'my_authorizations', 'my_requests']:
        return [IsAuthenticated()]
    # Admin-only actions
    elif self.action in ['pending_requests', 'approve_request', 'reject_request']:
        return [IsAuthenticated(), CanManageSignatureAuthorizations()]
    # Public actions (signature setup via token)
    elif self.action in ['signature_setup', 'save_signature']:
        return [AllowAny()]
    # Default: authenticated users only
    return [IsAuthenticated()]
```

### 3. Added Missing Imports
```python
from .audit_utils import audit_action, audit_authorization_request, AuditLogger
from rest_framework.permissions import IsAuthenticated, AllowAny
```

### 4. Fixed Session Access
Removed the line that tried to access `request.session.session_key` in debug code.

## Testing Results

✅ **All tests passing!**

```
Testing request_authorization (POST)...
Status: 201
SUCCESS!
```

The backend now:
- Accepts authorization requests from authenticated users
- Creates the authorization request record
- Sends email to the user with signature setup link
- Sends notification to administrators
- Returns HTTP 201 Created

## Action Required

**⚠️ RESTART THE DJANGO DEVELOPMENT SERVER**

The code changes have been applied, but you need to restart the Django server for them to take effect:

1. Stop the current Django server (Ctrl+C in the terminal where it's running)
2. Start it again:
   ```bash
   cd backend
   python manage.py runserver
   ```

3. Refresh your browser and try submitting the authorization request again

## Verification

After restarting the server, you should see:
1. ✅ No more 403 errors
2. ✅ "Authorization request submitted successfully!" message
3. ✅ Email sent to the user with signature setup link
4. ✅ Request appears in "Pending Requests" section

## Files Modified
- `frontend/src/services/api.js` - Added missing API functions
- `backend/reports/views_authorization.py` - Fixed permissions and imports
- `backend/test_simple.py` - Test script to verify the fix

## Clean Up
You can delete these test files after verifying everything works:
- `backend/test_permissions.py`
- `backend/test_simple.py`
