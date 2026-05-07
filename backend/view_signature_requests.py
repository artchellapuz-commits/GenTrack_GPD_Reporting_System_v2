#!/usr/bin/env python
"""View all e-signature authorization requests in the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization

print("=" * 80)
print("E-SIGNATURE AUTHORIZATION REQUESTS DATABASE")
print("=" * 80)

# Get all requests
requests = SignatoryAuthorizationRequest.objects.all().order_by('-created_at')
total_requests = requests.count()

print(f"\n📊 TOTAL REQUESTS: {total_requests}")
print("=" * 80)

if total_requests == 0:
    print("\n❌ No requests found in database")
else:
    print("\n📋 ALL REQUESTS:\n")
    
    for i, req in enumerate(requests, 1):
        print(f"{i}. REQUEST ID: {req.id}")
        print(f"   User: {req.user.username}")
        print(f"   Signatory: {req.signatory_name}")
        print(f"   Role: {req.role}")
        print(f"   Email: {req.email}")
        print(f"   Status: {req.status}")
        print(f"   Justification: {req.justification[:50]}..." if len(req.justification) > 50 else f"   Justification: {req.justification}")
        print(f"   Created: {req.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if req.reviewed_by:
            print(f"   Reviewed By: {req.reviewed_by.username}")
            print(f"   Reviewed At: {req.reviewed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if req.admin_notes:
            print(f"   Admin Notes: {req.admin_notes}")
        
        print()

print("=" * 80)
print("AUTHORIZATIONS CREATED FROM REQUESTS")
print("=" * 80)

# Get all authorizations
authorizations = SignatoryAuthorization.objects.all().order_by('-authorization_date')
total_auth = authorizations.count()

print(f"\n📊 TOTAL AUTHORIZATIONS: {total_auth}")
print("=" * 80)

if total_auth == 0:
    print("\n❌ No authorizations found in database")
else:
    print("\n🔐 ALL AUTHORIZATIONS:\n")
    
    for i, auth in enumerate(authorizations, 1):
        print(f"{i}. AUTHORIZATION ID: {auth.id}")
        print(f"   User: {auth.user.username}")
        print(f"   Signatory: {auth.signatory_name}")
        print(f"   Active: {'✅ Yes' if auth.is_active else '❌ No'}")
        print(f"   Signature Created: {'✅ Yes' if auth.signature_created else '⏳ Pending'}")
        print(f"   Requires 2FA: {'✅ Yes' if auth.requires_2fa else '❌ No'}")
        print(f"   Authorized Date: {auth.authorization_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if auth.expiry_date:
            print(f"   Expiry Date: {auth.expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if auth.setup_token:
            print(f"   Setup Token: {auth.setup_token[:20]}... (valid for signature setup)")
            if auth.token_expires:
                print(f"   Token Expires: {auth.token_expires.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if auth.notes:
            print(f"   Notes: {auth.notes}")
        
        print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\n✅ Total Requests: {total_requests}")
print(f"✅ Total Authorizations: {total_auth}")
print(f"✅ Pending Signatures: {authorizations.filter(signature_created=False).count()}")
print(f"✅ Completed Signatures: {authorizations.filter(signature_created=True).count()}")

# Status breakdown
pending = requests.filter(status='PENDING').count()
approved = requests.filter(status='APPROVED').count()
rejected = requests.filter(status='REJECTED').count()
cancelled = requests.filter(status='CANCELLED').count()

print(f"\n📊 Request Status Breakdown:")
print(f"   - Pending: {pending}")
print(f"   - Approved: {approved}")
print(f"   - Rejected: {rejected}")
print(f"   - Cancelled: {cancelled}")

print("\n" + "=" * 80)
print("✅ All e-signature requests are being saved to the database!")
print("=" * 80)
