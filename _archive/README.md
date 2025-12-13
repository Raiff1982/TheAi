# Codette Archive Directory

**Created**: December 5, 2025  
**Purpose**: Archive of legacy Codette implementations and supporting files

---

## ?? What's Archived Here

This directory contains legacy Codette implementations that have been superseded by the current production system. Files are preserved for historical reference and potential recovery.

### Directory Structure

```
_archive/
??? v0_original/              # Original pre-ML implementation
?   ??? codette.py           # Original Codette class
?   ??? codette.py.backup    # Manual backup
?   ??? codette.py.bak       # Additional backup
?
??? v1_implementations/       # Experimental implementations
?   ??? codette_advanced.py  # Advanced features prototype
?   ??? codette_hybrid.py    # Hybrid ML/rule-based system
?
??? servers/                  # Legacy server implementations
?   ??? v1/                  # Original server
?   ?   ??? codette_server.py
?   ??? v2/                  # Production-optimized server
?       ??? codette_server_production.py
?
??? interfaces/               # Old interface layers
?   ??? codette_interface.py (2 variants)
?
??? tests/                    # Obsolete test files
?   ??? test_codette_hybrid_integration.py
?
??? build_specs/              # Build configurations
    ??? codette_hybrid.spec   # PyInstaller spec
```

---

## ?? Current Active Files (NOT in Archive)

- **`Codette/codette_new.py`** - Primary ML-powered implementation
- **`codette_server_unified.py`** (root) - Unified server with all features
- **Frontend integration** - React hooks and TypeScript clients

---

## ?? Migration Summary

### Files Archived
- ? 3 original implementation files (codette.py + backups)
- ? 2 experimental implementations (advanced + hybrid)
- ? 3 legacy server files
- ? 2 interface layer files
- ? 1 test file
- ? 1 build spec file

**Total**: 12 files archived

### Reason for Archival
Each archived file was superseded by newer implementations:

1. **Original `codette.py`** ? Replaced by `codette_new.py` with ML capabilities
2. **Advanced/Hybrid versions** ? Features integrated into `codette_new.py`
3. **Multiple servers** ? Consolidated into `codette_server_unified.py`
4. **Interface layers** ? Direct API calls via unified server
5. **Hybrid tests** ? Obsolete with new architecture

---

## ?? Finding Specific Features

If you need to reference old implementations:

### Original Codette Logic
- **Location**: `v0_original/codette.py`
- **Features**: Basic chat, simple responses
- **Note**: Pre-ML, no sentiment analysis

### Advanced Features
- **Location**: `v1_implementations/codette_advanced.py`
- **Features**: Enhanced perspectives, creative responses
- **Note**: Prototype for ML integration

### Hybrid System
- **Location**: `v1_implementations/codette_hybrid.py`
- **Features**: ML + rule-based hybrid approach
- **Note**: Experimental, features now in `codette_new.py`

### Production Server
- **Location**: `servers/v2/codette_server_production.py`
- **Features**: Optimized endpoints, caching
- **Note**: Features merged into `codette_server_unified.py`

---

## ?? Important Notes

1. **Do NOT delete these files** - They preserve development history
2. **Do NOT import from archive** - Use active files only
3. **Reference only** - These files are not maintained
4. **Git tracking** - Archive should be committed to preserve history

---

## ?? Restoring Archived Files

If you need to restore a file:

```powershell
# Example: Restore codette_hybrid.py
Copy-Item "Codette\_archive\v1_implementations\codette_hybrid.py" "Codette\"
```

**Warning**: Restoring files may cause import conflicts. Review active implementation first.

---

## ?? Archive Statistics

- **Total archived size**: ~4000 lines of Python code
- **Oldest file**: codette.py (original implementation)
- **Most recent**: codette_hybrid.py (last experimental version)
- **Archive date**: December 5, 2025

---

## ?? See Also

- [CODETTE_FILE_STRUCTURE.md](../../CODETTE_FILE_STRUCTURE.md) - Complete file organization
- [Codette/codette_new.py](../codette_new.py) - Current active implementation
- [codette_server_unified.py](../../codette_server_unified.py) - Current server

---

**Status**: ? Archive complete and organized  
**Maintained**: No (reference only)  
**Last updated**: December 5, 2025
