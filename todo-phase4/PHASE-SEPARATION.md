# Phase Separation Guide

## Current Status

This repository contains work for **multiple phases** of the Todo Evolution project. This document clarifies which directories belong to which phase.

## Phase I: In-Memory CLI Application (Current Branch: 1-in-memory-todo)

**Status**: Specified, planned, ready for implementation

**Scope**: Command-line todo application with in-memory storage

**Implementation Location**:
- `src/` - Phase I source code (CLI application)
- `specs/1-in-memory-todo/` - Phase I specifications

**Constraints** (per constitution):
- ✅ CLI only (no web UI)
- ✅ In-memory storage (no database)
- ✅ Python 3.13+ with standard library
- ✅ Single process, single user
- ✅ Data lost on exit

**Implementation Status**: Not yet started (ready for `/sp.implement`)

---

## Phase II: Web Application (Future Work)

**Status**: Preliminary work exists but NOT specified or planned

**Scope**: Web-based todo application with database persistence

**Implementation Location**:
- `backend/` - Phase II backend (FastAPI + PostgreSQL)
- `frontend/` - Phase II frontend (Next.js)

**Constraints** (per constitution):
- ✅ Web framework allowed (FastAPI)
- ✅ Database allowed (PostgreSQL)
- ✅ Web UI allowed (Next.js/React)
- ❌ Must maintain Task entity invariance (id, title, status)

**Implementation Status**: Preliminary code exists but lacks formal specification

---

## Important Notes

### For Phase I Implementation

When running `/sp.implement` for Phase I:
- **Ignore** `backend/` and `frontend/` directories
- **Implement** in `src/` directory as specified in `specs/1-in-memory-todo/plan.md`
- **Follow** the structure: `src/models/`, `src/services/`, `src/cli/`

### For Phase II Work

Phase II requires:
1. Complete Phase I first
2. Create `specs/2-web-application/spec.md`
3. Run `/sp.plan` for Phase II
4. Run `/sp.tasks` for Phase II
5. Then implement or integrate existing backend/frontend code

### Directory Isolation

- Phase I code: `src/` (CLI application)
- Phase II code: `backend/` + `frontend/` (web application)
- These are **separate implementations** and should not be mixed

---

## Recommended Next Steps

1. **Complete Phase I**: Run `/sp.implement` to build the CLI application in `src/`
2. **Test Phase I**: Validate all user stories work independently
3. **Specify Phase II**: Create formal specification for web application
4. **Integrate or Rewrite**: Decide whether to use existing backend/frontend or start fresh

---

**Last Updated**: 2026-01-07
