#!/usr/bin/env python3
"""
HuggingFace Authentication Setup Helper

This script helps you authenticate with HuggingFace to access the Llama model.
"""

import sys
import os
from huggingface_hub import HfFolder, login, whoami


def main():
    print("=" * 70)
    print("HuggingFace Authentication Setup")
    print("=" * 70)
    
    # Check if already authenticated
    print("\n[1/3] Checking current authentication status...")
    try:
        token = HfFolder.get_token()
        if token:
            try:
                user = whoami()
                print(f"✓ Already authenticated as: {user['name']}")
                print(f"✓ Token found in cache")
                
                # Check if we can access the model
                print("\n[2/3] Testing model access...")
                try:
                    from transformers import AutoTokenizer
                    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
                    print("✓ Successfully accessed Llama-3.2-1B-Instruct model!")
                    print("\nYou're all set! You can now run:")
                    print("  python3 test_llama_classifier.py")
                    return
                except Exception as e:
                    error_msg = str(e).lower()
                    if "gated" in error_msg or "401" in error_msg or "access" in error_msg:
                        print("⚠ Authentication works, but you need to request model access.")
                        print("\nPlease visit:")
                        print("  https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct")
                        print("\nClick 'Agree and access repository' and accept the license.")
                        print("Then run this script again to verify access.")
                        return
                    else:
                        print(f"⚠ Error accessing model: {e}")
                        print("This might be a network or model loading issue.")
                        return
            except Exception as e:
                print(f"⚠ Token found but validation failed: {e}")
                print("Let's set up a new token...")
        else:
            print("✗ No token found")
    except Exception as e:
        print(f"✗ Error checking authentication: {e}")
    
    # Check environment variable
    print("\n[2/3] Checking environment variables...")
    hf_token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_TOKEN')
    if hf_token:
        print("✓ Found HF_TOKEN environment variable")
        try:
            login(token=hf_token)
            user = whoami()
            print(f"✓ Successfully authenticated as: {user['name']}")
            print("\nYou can now run:")
            print("  python3 test_llama_classifier.py")
            return
        except Exception as e:
            print(f"✗ Token validation failed: {e}")
            print("Please check your token and try again.")
    
    # Interactive login
    print("\n[3/3] Setting up authentication...")
    print("\nTo authenticate, you need a HuggingFace access token.")
    print("\nSteps:")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Click 'New token'")
    print("3. Give it a name (e.g., 'llama-classifier')")
    print("4. Select 'Read' access")
    print("5. Click 'Generate token'")
    print("6. Copy the token (starts with 'hf_...')")
    print("\nThen:")
    print("  Option A: Run this script with your token:")
    print("    python3 setup_hf_auth.py YOUR_TOKEN_HERE")
    print("\n  Option B: Set environment variable:")
    print("    export HF_TOKEN=your_token_here")
    print("    python3 setup_hf_auth.py")
    print("\n  Option C: Enter token interactively below:")
    
    # Try to get token from command line
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
        if token.startswith('hf_'):
            print(f"\nUsing token from command line...")
            try:
                login(token=token)
                user = whoami()
                print(f"✓ Successfully authenticated as: {user['name']}")
                
                # Test model access
                print("\nTesting model access...")
                try:
                    from transformers import AutoTokenizer
                    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
                    print("✓ Successfully accessed Llama-3.2-1B-Instruct model!")
                    print("\nYou're all set! You can now run:")
                    print("  python3 test_llama_classifier.py")
                except Exception as e:
                    error_msg = str(e).lower()
                    if "gated" in error_msg or "401" in error_msg or "access" in error_msg:
                        print("⚠ Authentication works, but you need to request model access.")
                        print("\nPlease visit:")
                        print("  https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct")
                        print("\nClick 'Agree and access repository' and accept the license.")
                        print("Then run this script again to verify access.")
                    else:
                        print(f"⚠ Error accessing model: {e}")
                return
            except Exception as e:
                print(f"✗ Authentication failed: {e}")
                print("Please check your token and try again.")
                return
        else:
            print("✗ Invalid token format. Token should start with 'hf_'")
            return
    
    # Interactive input
    print("\nEnter your HuggingFace token (or press Enter to skip):")
    try:
        token = input("Token: ").strip()
        if token:
            if token.startswith('hf_'):
                try:
                    login(token=token)
                    user = whoami()
                    print(f"\n✓ Successfully authenticated as: {user['name']}")
                    
                    # Test model access
                    print("\nTesting model access...")
                    try:
                        from transformers import AutoTokenizer
                        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
                        print("✓ Successfully accessed Llama-3.2-1B-Instruct model!")
                        print("\nYou're all set! You can now run:")
                        print("  python3 test_llama_classifier.py")
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "gated" in error_msg or "401" in error_msg or "access" in error_msg:
                            print("⚠ Authentication works, but you need to request model access.")
                            print("\nPlease visit:")
                            print("  https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct")
                            print("\nClick 'Agree and access repository' and accept the license.")
                            print("Then run this script again to verify access.")
                        else:
                            print(f"⚠ Error accessing model: {e}")
                except Exception as e:
                    print(f"\n✗ Authentication failed: {e}")
                    print("Please check your token and try again.")
            else:
                print("✗ Invalid token format. Token should start with 'hf_'")
        else:
            print("\nSkipped. You can authenticate later by:")
            print("  1. Setting HF_TOKEN environment variable")
            print("  2. Running: python3 setup_hf_auth.py YOUR_TOKEN")
            print("  3. Using huggingface-cli login (if installed)")
    except (EOFError, KeyboardInterrupt):
        print("\n\nCancelled. You can authenticate later.")


if __name__ == '__main__':
    main()
