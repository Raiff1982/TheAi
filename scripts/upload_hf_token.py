#!/usr/bin/env python3
"""
Codette Ultimate - Non-Interactive HF Upload
Usage: python upload_hf_token.py YOUR_HF_TOKEN
"""
import sys
from pathlib import Path
from huggingface_hub import HfApi, HfFolder

def upload_with_token(token):
    """Upload files using provided HF token"""
    print("=" * 70)
    print("🚀 CODETTE ULTIMATE - HUGGING FACE UPLOAD")
    print("=" * 70)
    
    # Save token
    print("\n[Step 1] Authenticating...")
    HfFolder.save_token(token)
    print("✅ Token saved")
    
    # Initialize API
    api = HfApi()
    repo_id = "Raiff1982/Codette-Ultimate"
    local_dir = r"j:\TheAI\models"
    
    # Create repo
    print("\n[Step 2] Creating repository...")
    try:
        repo_info = api.create_repo(
            repo_id=repo_id,
            repo_type="model",
            exist_ok=True,
            private=False
        )
        print(f"✅ Repository: {repo_info.url}")
    except Exception as e:
        print(f"Note: {e}")
    
    # Upload files
    files_to_upload = [
        ("Modelfile_Codette_Ultimate", "Modelfile_Codette_Ultimate"),
        ("README_Codette_Ultimate.md", "README.md"),
        ("README_GPT_OSS.md", "docs/README_GPT_OSS.md"),
        ("README_RC_XI_CPU.md", "docs/README_RC_XI_CPU.md"),
        ("Modelfile_RC_XI_CPU", "docs/Modelfile_RC_XI_CPU"),
    ]
    
    print("\n[Step 3] Uploading files...")
    uploaded = 0
    for local_file, repo_path in files_to_upload:
        local_path = Path(local_dir) / local_file
        if local_path.exists():
            try:
                print(f"  → {local_file}")
                api.upload_file(
                    path_or_fileobj=str(local_path),
                    path_in_repo=repo_path,
                    repo_id=repo_id,
                    repo_type="model",
                    commit_message=f"Add {local_file}"
                )
                print(f"    ✅")
                uploaded += 1
            except Exception as e:
                print(f"    ❌ {str(e)[:80]}")
        else:
            print(f"  ⚠️ Not found: {local_file}")
    
    # Upload docs
    print("\n[Step 4] Uploading documentation...")
    audit_file = r"j:\TheAI\COMPREHENSIVE_CODETTE_CAPABILITIES_AUDIT.md"
    if Path(audit_file).exists():
        try:
            print(f"  → CAPABILITIES_AUDIT.md")
            api.upload_file(
                path_or_fileobj=audit_file,
                path_in_repo="docs/CAPABILITIES_AUDIT.md",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Add capabilities audit"
            )
            print(f"    ✅")
            uploaded += 1
        except Exception as e:
            print(f"    ❌ {str(e)[:80]}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ UPLOAD COMPLETE")
    print("=" * 70)
    print(f"\n📊 Statistics:")
    print(f"  • Files uploaded: {uploaded}")
    print(f"  • Repository: https://huggingface.co/{repo_id}")
    print(f"\n🎯 Your Codette Ultimate is now live!")
    print(f"  Users can access with:")
    print(f"    ollama pull Raiff1982/codette-ultimate")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_hf_token.py YOUR_HF_TOKEN")
        print("\nGet your token from: https://huggingface.co/settings/tokens")
        print("Token should start with 'hf_'")
        sys.exit(1)
    
    token = sys.argv[1]
    
    if not token.startswith("hf_"):
        print("⚠️  Token should start with 'hf_'")
        print("Get a new token from: https://huggingface.co/settings/tokens")
        sys.exit(1)
    
    try:
        upload_with_token(token)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
