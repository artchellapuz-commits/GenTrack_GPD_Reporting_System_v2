# 🔧 FIX: Emails Not Being Sent

## The Problem

You're not receiving emails because the system is configured to use **Console Backend** (development mode), which only prints emails to the Django console instead of actually sending them via SMTP.

## The Solution

I've configured the system to use Gmail SMTP, but you need to complete the setup by adding your Gmail App Password.

## Quick Setup (3 Steps)

### Step 1: Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Sign in to your Gmail account (cloudesunnet@gmail.com)
3. Select app: **"Mail"**
4. Select device: **"Other"** → Type: **"NPC Reporting"**
5. Click **"Generate"**
6. Copy the 16-character password (like: `abcd efgh ijkl mnop`)

**Note:** If you can't access App Passwords, you need to enable 2-Factor Authentication first:
- Go to https://myaccount.google.com/security
- Enable "2-Step Verification"
- Then try again

### Step 2: Update .env File

1. Open `backend/.env` file
2. Find this line:
   ```
   EMAIL_HOST_PASSWORD=your-gmail-app-password-here
   ```
3. Replace `your-gmail-app-password-here` with your App Password (remove spaces)
4. Save the file

Example:
```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

### Step 3: Restart Django Server

The server needs to be restarted to load the new configuration.

**Option A: Using the running server**
1. Find the terminal where Django is running
2. Press `Ctrl + C` to stop it
3. Run: `python manage.py runserver`

**Option B: Using Kiro (if server is running as background process)**
- The server will automatically reload when you save the .env file

## Test the Configuration

After completing the steps above, test if emails are working:

### Option 1: Run Test Script
```bash
cd backend
python test_email_sending.py
```

This will:
- Check your email configuration
- Send a test email to any address you specify
- Show any errors if something is wrong

### Option 2: Test with Real Request
1. Go to the signature request page
2. Submit a new authorization request
3. Use `cloudesunnet@gmail.com` as the email
4. Check your Gmail inbox (and spam folder)

## What Changed

### Before:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
- Emails printed to console only
- No real emails sent

### After:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=cloudesunnet@gmail.com
EMAIL_HOST_PASSWORD=[your-app-password]
DEFAULT_FROM_EMAIL=cloudesunnet@gmail.com
```
- Real emails sent via Gmail SMTP
- Emails arrive in inbox

## Verification

After setup, when you submit a signature request:

1. ✅ Email sent via Gmail SMTP
2. ✅ Arrives in the recipient's inbox within seconds
3. ✅ Contains signature setup link
4. ✅ Professional format

## Troubleshooting

### "Authentication failed" error?
- ✅ Make sure 2FA is enabled on Gmail
- ✅ Use App Password, not regular password
- ✅ Remove spaces from the password
- ✅ Make sure you're using the correct Gmail account

### Email not arriving?
- ✅ Check spam/junk folder
- ✅ Verify email address is correct
- ✅ Check Django console for errors
- ✅ Make sure server was restarted

### Still seeing console output?
- ✅ Make sure .env file was saved
- ✅ Make sure server was restarted
- ✅ Check EMAIL_BACKEND is set to smtp.EmailBackend

## Files Created

- `SETUP_GMAIL_FOR_EMAILS.md` - Detailed Gmail setup guide
- `backend/test_email_sending.py` - Test script
- `backend/TEST_EMAIL.bat` - Quick test batch file
- `backend/.env` - Updated with SMTP configuration

## Security

⚠️ **Important:**
- Never commit .env file to Git
- Never share your App Password
- App Password is different from your Gmail password
- You can revoke App Passwords anytime from Google Account settings

---

## Summary

**Current Status:** Email configuration updated, waiting for Gmail App Password

**Next Step:** 
1. Get Gmail App Password from https://myaccount.google.com/apppasswords
2. Update `EMAIL_HOST_PASSWORD` in `backend/.env`
3. Restart Django server
4. Test by submitting a signature request

**After setup:** Emails will be sent to the email address entered in the signature request form!
