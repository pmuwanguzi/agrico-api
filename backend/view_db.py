#!/usr/bin/env python
"""View database contents."""
from app import create_app, db
from app.models import User
from app.models.farm import Farm

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("DATABASE CONTENTS")
    print("="*60)
    
    # Users
    print("\n📋 USERS TABLE")
    print("-"*60)
    users = User.query.all()
    if users:
        for user in users:
            print(f"  ID: {user.id}")
            print(f"  Name: {user.full_name}")
            print(f"  Email: {user.email}")
            print(f"  Role: {user.role}")
            print(f"  Created: {user.created_at}")
            print()
    else:
        print("  (No users found)")
    
    # Farms
    print("\n🌾 FARMS TABLE")
    print("-"*60)
    farms = Farm.query.all()
    if farms:
        for farm in farms:
            print(f"  Farm ID: {farm.farm_id}")
            print(f"  User ID: {farm.user_id}")
            print(f"  Name: {farm.farm_name}")
            print(f"  Location: {farm.location}")
            print(f"  Size (acres): {farm.size_acres}")
            print(f"  Created: {farm.created_at}")
            print()
    else:
        print("  (No farms found)")
    
    print("="*60 + "\n")
