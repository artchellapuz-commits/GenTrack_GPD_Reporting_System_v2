# 📧 Setup Gmail to Send Real Emails

## Current Status

I've configured the system to use Gmail SMTP, but you need to provide your Gmail App Password.

## Steps to Get Gmail App Password

### 1. Enable 2-Factor Authentication (if not already enabled)

1. Go to https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the steps to enable it

### 2. Generate App Password

1. Go to https://myaccount.google.com/apppasswords
2. You might need to sign in again
3. In the "Select app" dropdown, choose **"Mail"**
4. In the "Select device" dropdown, choose **"Other (Custom name)"**
5. Type: **"NPC Reporting System"**
6. Click **"Generate"**
7. Google will show you a 16-character password (like: `abcd efgh ijkl mnop`)
8. **Copy this password** (you won't be able to see it again)

### 3. Update the .env File

1. Open `backend/.env` file
2. Find the line: `EMAIL_HOST_PASSWORD=your-gmail-app-password-here`
3. Replace `your-gmail-app-password-here` with the 16-character password
4. Remove any spaces from the password
5. Save the file

Example:
```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

### 4. Restart the Django Server

Stop and restart the Django server to load the new configuration:

```bash
# Stop the server (Ctrl+C)
# Then restart:
cd backend
python manage.py runserver
```

## Alternative: Use a Different Email

If you want to use a different Gmail account:

1. Update `EMAIL_HOST_USER` in `.env` to your email
2. Update `DEFAULT_FROM_EMAIL` to the same email
3. Generate an App Password for that account
4. Update `EMAIL_HOST_PASSWORD` with the App Password

## Testing

After setting up:

1. Submit a signature authorization request
2. Check the email inbox (cloudesunnet@gmail.com)
3. The email should arrive within a few seconds
4. Check spam folder if you don't see it

## Troubleshooting

### "Authentication failed" error?
- Make sure 2FA is enabled on your Google account
- Make sure you're using an App Password, not your regular password
- Make sure there are no spaces in the password

### Email not arriving?
- Check spam/junk folder
- Make sure the email address in the request form is correct
- Check Django console for error messages

### Still using console backend?
- Make sure you saved the .env file
- Make sure you restarted the Django server
- Check that EMAIL_BACKEND is set to smtp.EmailBackend

## Security Note

⚠️ **Never commit the .env file to Git!**
- The .env file contains sensitive passwords
- It should already be in .gitignore
- Never share your App Password

## Current Configuration

After you add the App Password, the system will:
- ✅ Send real emails via Gmail SMTP
- ✅ Use cloudesunnet@gmail.com as the sender
- ✅ Send to whatever email is entered in the request form
- ✅ Include the signature setup link

---

**Next Step:** Get your Gmail App Password and update the .env file!
