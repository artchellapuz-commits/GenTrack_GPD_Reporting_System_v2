# 🔧 Frontend Signature Integration Guide

## ⚠️ Current Issue

The signatures are vanishing because **the frontend is not calling the save endpoint** when signatures are drawn.

## ✅ Backend is Ready

The backend has everything needed:
- ✅ `save-drawn-signature` endpoint created
- ✅ Database models ready
- ✅ Dynamic signature loading implemented
- ✅ API method added to `frontend/src/services/api.js`

## 🔧 What Needs to be Done in Frontend

### 1. Find the Signature Drawing Component

Look for the component where users draw signatures in the preview. It's likely in:
- `frontend/src/components/ReportPreview.vue`
- `frontend/src/components/SignatureCanvas.vue`
- `frontend/src/views/Reports/Preview.vue`

### 2. Add Save Functionality

When a signature is drawn and saved, call the API:

```javascript
import { api } from '@/services/api';

// In your signature component
async function saveSignature(signatureData, signatoryInfo) {
  try {
    const response = await api.saveDrawnSignature({
      signatory_name: signatoryInfo.name,        // e.g., "O.M. LAVA"
      signatory_role: signatoryInfo.role,        // e.g., "Prepared by:"
      report_date: reportDate,                    // e.g., "2026-05-07"
      report_type: 'PSR',                         // or 'DAILY'
      signature: signatureData                    // base64 data URL
    });
    
    console.log('✅ Signature saved:', response.data);
    
    // Show success message
    alert('Signature saved successfully!');
    
    // Optionally reload preview to show the saved signature
    await loadPreview();
    
  } catch (error) {
    console.error('❌ Failed to save signature:', error);
    alert('Failed to save signature: ' + error.message);
  }
}
```

### 3. Example Integration

Here's a complete example of how to integrate signature saving:

```vue
<template>
  <div class="signature-section">
    <h3>{{ signatoryInfo.role }}</h3>
    <p>{{ signatoryInfo.name }}</p>
    
    <!-- Show existing signature if available -->
    <div v-if="signatoryInfo.has_signature" class="existing-signature">
      <img :src="signatoryInfo.signature_url" alt="Signature" />
      <button @click="redrawSignature">Redraw Signature</button>
    </div>
    
    <!-- Show signature canvas if drawing -->
    <div v-else-if="isDrawing" class="signature-canvas">
      <canvas ref="signatureCanvas" 
              @mousedown="startDrawing"
              @mousemove="draw"
              @mouseup="stopDrawing"
              width="400" 
              height="150">
      </canvas>
      <div class="signature-actions">
        <button @click="clearSignature">Clear</button>
        <button @click="saveCurrentSignature">Save Signature</button>
        <button @click="cancelDrawing">Cancel</button>
      </div>
    </div>
    
    <!-- Show draw button if no signature -->
    <div v-else>
      <button @click="startDrawingMode">Draw Signature</button>
    </div>
  </div>
</template>

<script>
import { api } from '@/services/api';

export default {
  name: 'SignatureSection',
  props: {
    signatoryInfo: {
      type: Object,
      required: true
    },
    reportDate: {
      type: String,
      required: true
    },
    reportType: {
      type: String,
      default: 'PSR'
    }
  },
  data() {
    return {
      isDrawing: false,
      canvas: null,
      ctx: null,
      drawing: false,
      lastX: 0,
      lastY: 0
    };
  },
  methods: {
    startDrawingMode() {
      this.isDrawing = true;
      this.$nextTick(() => {
        this.canvas = this.$refs.signatureCanvas;
        this.ctx = this.canvas.getContext('2d');
        this.ctx.strokeStyle = '#000';
        this.ctx.lineWidth = 2;
        this.ctx.lineCap = 'round';
      });
    },
    
    startDrawing(e) {
      this.drawing = true;
      const rect = this.canvas.getBoundingClientRect();
      this.lastX = e.clientX - rect.left;
      this.lastY = e.clientY - rect.top;
    },
    
    draw(e) {
      if (!this.drawing) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      this.ctx.beginPath();
      this.ctx.moveTo(this.lastX, this.lastY);
      this.ctx.lineTo(x, y);
      this.ctx.stroke();
      
      this.lastX = x;
      this.lastY = y;
    },
    
    stopDrawing() {
      this.drawing = false;
    },
    
    clearSignature() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },
    
    async saveCurrentSignature() {
      try {
        // Get signature as base64 data URL
        const signatureData = this.canvas.toDataURL('image/png');
        
        // Check if canvas is empty
        const isBlank = !this.ctx
          .getImageData(0, 0, this.canvas.width, this.canvas.height).data
          .some(channel => channel !== 0);
        
        if (isBlank) {
          alert('Please draw a signature first');
          return;
        }
        
        // Save to backend
        const response = await api.saveDrawnSignature({
          signatory_name: this.signatoryInfo.name,
          signatory_role: this.signatoryInfo.role,
          report_date: this.reportDate,
          report_type: this.reportType,
          signature: signatureData
        });
        
        console.log('✅ Signature saved:', response.data);
        
        // Update the signatory info with the saved signature
        this.$emit('signature-saved', {
          ...this.signatoryInfo,
          has_signature: true,
          signature_url: response.data.signature_url,
          signed_at: new Date().toISOString()
        });
        
        // Exit drawing mode
        this.isDrawing = false;
        
        // Show success message
        alert('Signature saved successfully!');
        
      } catch (error) {
        console.error('❌ Failed to save signature:', error);
        alert('Failed to save signature: ' + (error.response?.data?.error || error.message));
      }
    },
    
    cancelDrawing() {
      this.isDrawing = false;
    },
    
    redrawSignature() {
      this.isDrawing = true;
    }
  }
};
</script>

<style scoped>
.signature-section {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
}

.signature-canvas canvas {
  border: 2px solid #000;
  cursor: crosshair;
  background: white;
}

.signature-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.existing-signature img {
  max-width: 200px;
  border: 1px solid #ddd;
  padding: 5px;
  background: white;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #007bff;
  color: white;
}

button:hover {
  background: #0056b3;
}
</style>
```

### 4. Update Preview Component

In your main preview component, make sure to:

1. **Pass report date to signature components:**
```javascript
<SignatureSection
  v-for="(sig, index) in signatures.first_row"
  :key="index"
  :signatory-info="sig"
  :report-date="reportDate"
  :report-type="reportType"
  @signature-saved="handleSignatureSaved"
/>
```

2. **Handle signature saved event:**
```javascript
methods: {
  handleSignatureSaved(updatedSignatory) {
    // Update the signature in the preview data
    const rowIndex = this.signatures.first_row.findIndex(
      sig => sig.name === updatedSignatory.name && sig.role === updatedSignatory.role
    );
    
    if (rowIndex !== -1) {
      this.$set(this.signatures.first_row, rowIndex, updatedSignatory);
    }
    
    // Optionally reload the entire preview
    // this.loadPreview();
  }
}
```

### 5. Ensure Report Date is Available

Make sure the report date is stored when generating the preview:

```javascript
data() {
  return {
    reportDate: null,  // Store the report date
    reportType: 'PSR',
    previewData: null,
    signatures: {
      first_row: [],
      second_row: []
    }
  };
},

methods: {
  async generatePreview(formData) {
    try {
      // Store the report date
      this.reportDate = formData.start_date;
      this.reportType = formData.report_type || 'PSR';
      
      // Generate preview
      const response = await api.previewReport(formData);
      this.previewData = response.data;
      this.signatures = response.data.signatures || { first_row: [], second_row: [] };
      
    } catch (error) {
      console.error('Failed to generate preview:', error);
    }
  }
}
```

## 🧪 Testing Steps

### Step 1: Verify API Method Works

Open browser console and test:

```javascript
// Test the API method directly
import { api } from '@/services/api';

const testSignature = {
  signatory_name: "O.M. LAVA",
  signatory_role: "Prepared by:",
  report_date: "2026-05-07",
  report_type: "PSR",
  signature: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
};

api.saveDrawnSignature(testSignature)
  .then(response => console.log('✅ Success:', response.data))
  .catch(error => console.error('❌ Error:', error));
```

### Step 2: Check Backend Logs

After calling the API, check Django console for:

```
🖊️ Saving drawn signature for report...
✅ User is admin, can sign for O.M. LAVA
✅ Signature file saved: /path/to/file
✅ ESignature record created: ID=1
✅ ReportSignature created: ID=1
```

### Step 3: Verify Database

Run the check script:

```bash
cd backend
python check_report_signatures.py
```

Should show:
```
📊 Total ReportSignatures in database: 1
Recent ReportSignatures:
  - ID: 1, Date: 2026-05-07, Type: PSR
    Signatory: O.M. LAVA (Prepared by:)
```

### Step 4: Test Preview Reload

1. Generate preview for 2026-05-07
2. Draw and save a signature
3. Reload the page
4. Generate preview for 2026-05-07 again
5. **Signature should appear automatically!** ✅

## 📝 Quick Fix for Testing

If you want to test quickly without modifying the frontend, you can use the browser console:

```javascript
// 1. Draw a signature on canvas (manually)
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'black';
ctx.fillRect(10, 10, 100, 50);

// 2. Get signature data
const signatureData = canvas.toDataURL('image/png');

// 3. Save to backend
fetch('http://localhost:8000/api/report-signatures/save-drawn-signature/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
  },
  body: JSON.stringify({
    signatory_name: "O.M. LAVA",
    signatory_role: "Prepared by:",
    report_date: "2026-05-07",
    report_type: "PSR",
    signature: signatureData
  })
})
.then(r => r.json())
.then(data => console.log('✅ Saved:', data))
.catch(err => console.error('❌ Error:', err));

// 4. Reload preview to see the signature persist
```

## 🎯 Summary

**Backend:** ✅ Ready (API endpoint created, database models ready)
**Frontend:** ⚠️ Needs integration (call `api.saveDrawnSignature()` when signature is drawn)

**Next Steps:**
1. Find the signature drawing component in frontend
2. Add call to `api.saveDrawnSignature()` when user saves signature
3. Pass `report_date` and `report_type` to signature components
4. Test by drawing signature, reloading, and verifying it persists

---

**Once the frontend calls the save endpoint, signatures will persist across reloads!** 🎉
