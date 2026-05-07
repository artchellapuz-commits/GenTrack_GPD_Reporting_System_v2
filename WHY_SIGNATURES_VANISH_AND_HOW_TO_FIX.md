# ⚠️ Why Signatures Vanish and How to Fix It

## 🔍 The Problem

Signatures are vanishing after reload because **the frontend is not saving them to the database**.

## 🎯 Root Cause

The backend is ready and working, but the frontend needs to be updated to call the save endpoint when a signature is drawn.

### What's Happening Now:

```
User draws signature
↓
Signature displayed in preview (in memory only)
↓
User reloads page
↓
Memory cleared
↓
Signature vanishes ❌
```

### What Should Happen:

```
User draws signature
↓
Frontend calls api.saveDrawnSignature() ✅
↓
Backend saves to database ✅
↓
Signature displayed in preview
↓
User reloads page
↓
Backend loads signature from database ✅
↓
Signature appears automatically ✅
```

## ✅ Backend Status

| Component | Status | Details |
|-----------|--------|---------|
| API Endpoint | ✅ READY | `/api/report-signatures/save-drawn-signature/` |
| Database Models | ✅ READY | `ESignature`, `ReportSignature` |
| Dynamic Loading | ✅ READY | `_get_report_signatures()` method |
| API Method | ✅ READY | `api.saveDrawnSignature()` in `api.js` |

## ⚠️ Frontend Status

| Component | Status | Action Needed |
|-----------|--------|---------------|
| Signature Drawing | ✅ EXISTS | Already implemented |
| Save to Database | ❌ MISSING | **Need to call `api.saveDrawnSignature()`** |
| Pass Report Date | ❓ UNKNOWN | Need to pass `report_date` to signature component |

## 🔧 Quick Fix

### Option 1: Test via Browser Console (Immediate)

1. **Login to the system**
2. **Generate a preview** for today's date
3. **Open browser console** (F12)
4. **Paste this code:**

```javascript
// Test saving a signature
fetch('http://localhost:8000/api/report-signatures/save-drawn-signature/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  },
  body: JSON.stringify({
    signatory_name: "O.M. LAVA",
    signatory_role: "Prepared by:",
    report_date: "2026-05-07",  // Use today's date
    report_type: "PSR",
    signature: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  })
})
.then(r => r.json())
.then(data => {
  console.log('✅ Signature saved:', data);
  alert('Signature saved! Reload the preview to see it persist.');
})
.catch(err => console.error('❌ Error:', err));
```

5. **Reload the preview** for the same date
6. **Signature should appear!** ✅

### Option 2: Update Frontend Code (Permanent Fix)

**File to modify:** Find the signature drawing component (likely in `frontend/src/components/` or `frontend/src/views/Reports/`)

**Add this code** when user saves a signature:

```javascript
import { api } from '@/services/api';

// When user clicks "Save Signature" button
async function saveSignature() {
  try {
    // Get signature from canvas
    const canvas = document.querySelector('canvas'); // or this.$refs.signatureCanvas
    const signatureData = canvas.toDataURL('image/png');
    
    // Save to backend
    const response = await api.saveDrawnSignature({
      signatory_name: this.signatoryInfo.name,     // e.g., "O.M. LAVA"
      signatory_role: this.signatoryInfo.role,     // e.g., "Prepared by:"
      report_date: this.reportDate,                 // e.g., "2026-05-07"
      report_type: this.reportType || 'PSR',
      signature: signatureData
    });
    
    console.log('✅ Signature saved:', response.data);
    alert('Signature saved successfully!');
    
    // Update UI to show saved signature
    this.signatoryInfo.has_signature = true;
    this.signatoryInfo.signature_url = response.data.signature_url;
    
  } catch (error) {
    console.error('❌ Failed to save signature:', error);
    alert('Failed to save signature: ' + error.message);
  }
}
```

## 📊 Verification Steps

### Step 1: Check if Signature Was Saved

After saving a signature, run this in backend:

```bash
cd backend
python check_report_signatures.py
```

**Expected output:**
```
📊 Total ReportSignatures in database: 1
Recent ReportSignatures:
  - ID: 1, Date: 2026-05-07, Type: PSR
    Signatory: O.M. LAVA (Prepared by:)
    Signed by: JMM_MATA
    Signed at: 2026-05-07 14:30:00
```

### Step 2: Check Server Logs

When saving a signature, Django console should show:

```
🖊️ Saving drawn signature for report...
✅ User is admin, can sign for O.M. LAVA
✅ Signature file saved: /path/to/file
✅ ESignature record created: ID=1
✅ ReportSignature created: ID=1
```

### Step 3: Test Persistence

1. Generate preview for 2026-05-07
2. Save a signature (via console or frontend)
3. Reload the page
4. Generate preview for 2026-05-07 again
5. **Signature should appear automatically!** ✅

## 🎯 Summary

**Problem:** Signatures vanish because they're not saved to database

**Cause:** Frontend doesn't call the save endpoint

**Solution:** Add `api.saveDrawnSignature()` call in frontend when signature is drawn

**Backend:** ✅ Ready and working
**Frontend:** ⚠️ Needs one line of code to call the save endpoint

**Quick Test:** Use browser console code above to test immediately

---

## 📝 Files Created for Reference

1. `FRONTEND_SIGNATURE_INTEGRATION_GUIDE.md` - Complete integration guide
2. `backend/check_report_signatures.py` - Check database script
3. `backend/test_save_signature_endpoint.py` - Test endpoint script
4. `frontend/src/services/api.js` - Updated with `saveDrawnSignature()` method

---

**Once the frontend calls `api.saveDrawnSignature()`, signatures will persist!** 🎉
