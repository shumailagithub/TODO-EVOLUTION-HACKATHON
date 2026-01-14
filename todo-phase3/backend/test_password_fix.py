#!/usr/bin/env python3
"""
Test script to verify the password hashing fix works correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth.password import hash_password, verify_password

def test_password_functions():
    print("Testing password hashing functions...")

    # Test 1: Basic functionality
    print("\n1. Testing basic password hashing and verification:")
    password = "testpassword123"
    hashed = hash_password(password)
    print(f"   Original: {password}")
    print(f"   Hashed: {hashed}")
    verified = verify_password(password, hashed)
    print(f"   Verification: {verified}")
    assert verified, "Basic password verification failed"
    print("   ✓ Basic functionality works")

    # Test 2: Long password (should be truncated)
    print("\n2. Testing long password (72+ characters):")
    long_password = "a" * 80  # 80 characters, longer than bcrypt's 72-byte limit
    hashed_long = hash_password(long_password)
    verified_long = verify_password(long_password, hashed_long)
    print(f"   Password length: {len(long_password)} characters")
    print(f"   Verification: {verified_long}")
    assert verified_long, "Long password verification failed"
    print("   ✓ Long password handling works")

    # Test 3: UTF-8 characters
    print("\n3. Testing UTF-8 characters:")
    utf8_password = "pässwörd_123_测试_москва"
    hashed_utf8 = hash_password(utf8_password)
    verified_utf8 = verify_password(utf8_password, hashed_utf8)
    print(f"   Original: {utf8_password}")
    print(f"   Verification: {verified_utf8}")
    assert verified_utf8, "UTF-8 password verification failed"
    print("   ✓ UTF-8 character handling works")

    # Test 4: Different passwords should not match
    print("\n4. Testing password mismatch:")
    password1 = "password1"
    password2 = "password2"
    hashed1 = hash_password(password1)
    verified_wrong = verify_password(password2, hashed1)
    print(f"   Trying '{password2}' against hash of '{password1}': {verified_wrong}")
    assert not verified_wrong, "Password mismatch test failed"
    print("   ✓ Password mismatch correctly detected")

    # Test 5: Same password, different hashes (due to salt)
    print("\n5. Testing that same password produces different hashes:")
    password_same = "same_password_for_test"
    hash1 = hash_password(password_same)
    hash2 = hash_password(password_same)
    print(f"   Hash 1: {hash1}")
    print(f"   Hash 2: {hash2}")
    print(f"   Are they different? {hash1 != hash2}")
    assert hash1 != hash2, "Same password should produce different hashes due to salt"
    print("   ✓ Different hashes generated (salt working)")

    # Test 6: Verify the first hash with the password
    verified_hash1 = verify_password(password_same, hash1)
    print(f"   Verification of hash1: {verified_hash1}")
    assert verified_hash1, "Verification of first hash failed"
    print("   ✓ First hash verifies correctly")

    # Test 7: Verify the second hash with the password
    verified_hash2 = verify_password(password_same, hash2)
    print(f"   Verification of hash2: {verified_hash2}")
    assert verified_hash2, "Verification of second hash failed"
    print("   ✓ Second hash verifies correctly")

    print("\n🎉 All tests passed! Password hashing fix is working correctly.")
    return True

if __name__ == "__main__":
    try:
        test_password_functions()
        print("\n✅ Password hashing functions are working correctly!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)