#!/usr/bin/env python3
"""
Codette Ultimate - Upload to Hugging Face Repository
This script uploads the complete Codette Ultimate model and documentation to HF Hub
"""

import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, Repository

def main():
    """Main upload function"""
    
    print("=" * 70)
    print("🚀 CODETTE ULTIMATE - HUGGING FACE REPOSITORY CREATION")
    print("=" * 70)
    
    # Configuration
    repo_id = "Raiff1982/Codette-Ultimate"
    repo_type = "model"
    local_dir = r"j:\TheAI\models"
    
    print(f"\n📍 Repository: {repo_id}")
    print(f"📁 Local Directory: {local_dir}")
    
    # Step 1: Initialize API
    print("\n[1/4] Initializing Hugging Face API...")
    try:
        api = HfApi()
        print("✅ HF API initialized")
    except Exception as e:
        print(f"❌ Error initializing API: {e}")
        return False
    
    # Step 2: Create/Get Repository
    print("\n[2/4] Creating/accessing repository...")
    try:
        # Try to create repo (won't fail if exists)
        repo_info = api.create_repo(
            repo_id=repo_id,
            repo_type=repo_type,
            exist_ok=True,
            private=False
        )
        print(f"✅ Repository ready: {repo_info.url}")
    except Exception as e:
        print(f"⚠️  Repository note: {e}")
    
    # Step 3: Upload Model Files
    print("\n[3/4] Uploading files...")
    
    files_to_upload = [
        ("Modelfile_Codette_Ultimate", "Modelfile_Codette_Ultimate"),
        ("README_Codette_Ultimate.md", "README.md"),
        ("README_GPT_OSS.md", "docs/README_GPT_OSS.md"),
        ("README_RC_XI_CPU.md", "docs/README_RC_XI_CPU.md"),
        ("Modelfile_RC_XI_CPU", "docs/Modelfile_RC_XI_CPU"),
    ]
    
    uploaded_count = 0
    for local_file, repo_path in files_to_upload:
        local_path = Path(local_dir) / local_file
        
        if local_path.exists():
            try:
                print(f"  Uploading: {local_file} → {repo_path}")
                api.upload_file(
                    path_or_fileobj=str(local_path),
                    path_in_repo=repo_path,
                    repo_id=repo_id,
                    repo_type=repo_type,
                    commit_message=f"Add {local_file}"
                )
                print(f"  ✅ {local_file}")
                uploaded_count += 1
            except Exception as e:
                print(f"  ⚠️  {local_file}: {e}")
        else:
            print(f"  ⚠️  File not found: {local_file}")
    
    
    # Step 4: Upload documentation
    print("\n[4/4] Uploading documentation...")
    doc_file = r"j:\TheAI\COMPREHENSIVE_CODETTE_CAPABILITIES_AUDIT.md"
    if Path(doc_file).exists():
        try:
            api.upload_file(
                path_or_fileobj=doc_file,
                path_in_repo="docs/CAPABILITIES_AUDIT.md",
                repo_id=repo_id,
                repo_type=repo_type,
                commit_message="Add comprehensive capabilities audit"
            )
            print("✅ Capabilities audit uploaded")
            uploaded_count += 1
        except Exception as e:
            print(f"⚠️  Capabilities audit: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"✅ UPLOAD COMPLETE")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  • Files uploaded: {uploaded_count}")
    print(f"  • Repository: https://huggingface.co/{repo_id}")
    print(f"  • Model Type: {repo_type}")
    
    print(f"\n🎯 Next Steps:")
    print(f"  1. Visit: https://huggingface.co/{repo_id}")
    print(f"  2. Review files and documentation")
    print(f"  3. Add model description and metadata")
    print(f"  4. Share with community!")
    
    print(f"\n💡 To use this model with Ollama:")
    print(f"  ollama pull Raiff1982/codette-ultimate")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
