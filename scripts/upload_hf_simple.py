#!/usr/bin/env python3
"""
Codette Ultimate - Upload to Hugging Face
"""
import os
from pathlib import Path
from huggingface_hub import HfApi, login

print("=" * 70)
print("🚀 CODETTE ULTIMATE - HUGGING FACE UPLOAD")
print("=" * 70)

# First, authenticate
print("\n[Step 1] Authenticating with Hugging Face Hub...")
print("Please follow the prompts to login with your Hugging Face account.")
try:
    login()
    print("✅ Authentication successful!\n")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)

# Initialize API
api = HfApi()
repo_id = "Raiff1982/Codette-Ultimate"
local_dir = r"j:\TheAI\models"

print(f"[Step 2] Creating repository: {repo_id}")
try:
    repo_info = api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        exist_ok=True,
        private=False
    )
    print(f"✅ Repository: {repo_info.url}\n")
except Exception as e:
    print(f"Note: {e}\n")

# Files to upload
files_to_upload = [
    ("Modelfile_Codette_Ultimate", "Modelfile_Codette_Ultimate"),
    ("README_Codette_Ultimate.md", "README.md"),
    ("README_GPT_OSS.md", "docs/README_GPT_OSS.md"),
    ("README_RC_XI_CPU.md", "docs/README_RC_XI_CPU.md"),
    ("Modelfile_RC_XI_CPU", "docs/Modelfile_RC_XI_CPU"),
]

print("[Step 3] Uploading model files...")
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
            print(f"    ✅ Uploaded to {repo_path}")
            uploaded += 1
        except Exception as e:
            print(f"    ⚠️ {str(e)[:100]}")
    else:
        print(f"  ⚠️ Not found: {local_file}")

# Upload capabilities audit
print("\n[Step 4] Uploading documentation...")
audit_file = r"j:\TheAI\COMPREHENSIVE_CODETTE_CAPABILITIES_AUDIT.md"
if Path(audit_file).exists():
    try:
        print(f"  → COMPREHENSIVE_CODETTE_CAPABILITIES_AUDIT.md")
        api.upload_file(
            path_or_fileobj=audit_file,
            path_in_repo="docs/CAPABILITIES_AUDIT.md",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Add comprehensive capabilities audit"
        )
        print(f"    ✅ Uploaded to docs/CAPABILITIES_AUDIT.md")
        uploaded += 1
    except Exception as e:
        print(f"    ⚠️ {str(e)[:100]}")

# Summary
print("\n" + "=" * 70)
print("✅ UPLOAD COMPLETE")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"  • Files uploaded: {uploaded}")
print(f"  • Repository: https://huggingface.co/{repo_id}")
print(f"\n🎯 Next Steps:")
print(f"  1. Visit: https://huggingface.co/{repo_id}")
print(f"  2. Review all uploaded files")
print(f"  3. Edit repo card/description")
print(f"  4. Share with community!")
print(f"\n💡 Model is ready for use!")
print("=" * 70)
