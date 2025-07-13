# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Start the full application:**
```bash
docker-compose up --build
```

**Frontend development (Vue.js):**
```bash
cd budget-vue
npm run dev        # Start development server
npm run build      # Build for production
npm run preview    # Preview production build
```

**Backend development (FastAPI):**
```bash
cd budget-backend
python -m uvicorn app.main:app --reload
```

**Development URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Database Admin: http://localhost:8080 (phpMyAdmin)
- Database: localhost:3306

## Architecture Overview

This is a full-stack budget tracking application with real bank data integration:

**Data Flow:**
- Bank → Fintable → Airtable → Local MySQL → Frontend
- Automatic daily sync from Airtable to local database
- Manual sync trigger available from frontend
- Smart Airtable cleanup (keeps 4 months, deletes older records)

**Backend (FastAPI + Python):**
- `budget-backend/app/main.py`: Main application with API endpoints
- `budget-backend/app/services/`: Core business logic
  - `auth_service.py`: JWT authentication with refresh tokens
  - `airtable_service.py`: Airtable API integration
  - `sync_service.py`: Background sync between Airtable and local DB
- `budget-backend/app/core/`: Infrastructure
  - `database.py`: MySQL database operations
  - `constants.py`: Configuration constants
  - `logger.py`: Logging setup
- `budget-backend/app/models/schemas.py`: Pydantic data models

**Frontend (Vue 3 + TypeScript):**
- `budget-vue/src/main.js`: App initialization with axios interceptors for token refresh
- `budget-vue/src/router/index.js`: Vue Router configuration with auth guards
- `budget-vue/src/stores/localStorage.ts`: Pinia stores for state management (accounts, transactions, user)
- `budget-vue/src/views/`: Main application pages (Home, Transactions, Profile, Login, CreateUser, ConnectToBank)
- `budget-vue/src/components/`: Reusable Vue components
- `budget-vue/src/types/aliases.ts`: TypeScript type definitions

**Authentication:**
- JWT tokens with automatic refresh via axios interceptors
- HttpOnly cookies for secure token storage
- Protected routes require authentication dependency

**Database:**
- MySQL 8.0 with PyMySQL driver
- Database schema in `budget-backend/sql/create.sql`
- Docker volume for data persistence

## Environment Configuration

**Backend requires `.env` file:**
- Airtable API credentials
- Database connection details
- JWT secrets

**Frontend requires `.env` file:**
- `VITE_BACKEND_URL=http://localhost:8000`

## Key Features

- Real bank transaction data via Fintable/Airtable integration
- Automatic background sync service that starts with the application
- Manual sync trigger from frontend
- JWT authentication with automatic token refresh
- Offline development capability with local database
- Docker development environment with hot reload
- Intelligent Airtable record management to stay within free tier limits

## Development Notes

- Uses Docker Compose for full-stack development
- Frontend has hot reload enabled with file polling for Docker
- Backend runs with uvicorn reload for development
- Database includes phpMyAdmin for easy data inspection
- CORS configured for cross-origin requests between frontend and backend
- Axios configured with automatic token refresh interceptors

## MCP Server Configuration

This project uses Model Context Protocol (MCP) servers for enhanced AI assistance. The following MCP servers are available and should be used automatically when relevant:

### Core MCP Servers

**1. Sequential Thinking Server (`mcp__sequential-thinking-docker__sequentialthinking`):**
- **Auto-use for:** Complex multi-step problems, architectural analysis, debugging complex issues, performance optimization, security analysis, more or less use it for everything - you cant go wrong
- **Capabilities:** Dynamic problem-solving with flexible thinking process, hypothesis generation and verification
- **Required when:** Problem requires 3+ steps, uncertainty exists, course correction may be needed, or complex analysis is involved
- **Examples:** Authentication flow analysis, database optimization, feature implementation planning

**2. Context7 Documentation Server (`mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs`):**
- **Auto-use for:** ANY mention of external libraries, frameworks, or APIs
- **Capabilities:** Current, comprehensive documentation with code examples
- **Required workflow:** Always call `resolve-library-id` first, then `get-library-docs` with the returned ID
- **Critical libraries:** Vue 3, FastAPI, Pinia, MySQL, Docker, Airtable API, JWT, TypeScript, Vite, Axios
- **Use immediately when:** User mentions library names, asks about API usage, needs implementation examples, or encounters library-specific errors

**3. IDE Integration Server (`mcp__ide__getDiagnostics` + `mcp__ide__executeCode`):**
- **Auto-use for:** Code validation, error checking, Python testing
- **Capabilities:** VS Code diagnostics, Python code execution in Jupyter kernel
- **Required after:** Making code changes, before committing, when debugging errors
- **Use for:** Validating TypeScript, checking lint errors, testing Python functions, verifying code syntax

### Automatic MCP Usage Rules

**ALWAYS use Context7 when user mentions:**
- Framework names: Vue, FastAPI, Pinia, Vite
- Database: MySQL, PyMySQL, SQL queries
- Libraries: Axios, JWT, Docker, TypeScript
- APIs: Airtable, authentication, REST endpoints

**ALWAYS use Sequential Thinking when:**
- User asks for implementation strategy
- Problem involves multiple components/files
- Security or authentication is involved
- Performance optimization is needed
- Architecture decisions are required
- Debugging complex multi-step issues

**ALWAYS use IDE Integration when:**
- Making code changes (run diagnostics after)
- Testing Python backend functionality
- Validating syntax or type checking
- User reports errors or warnings

### MCP Integration Examples

**Frontend Development:**
```
User: "How do I implement Vue 3 reactive forms?"
→ Auto-use: Context7 for Vue 3 docs + Sequential Thinking for implementation strategy
```

**Backend Development:**
```
User: "Add JWT refresh token logic to FastAPI"
→ Auto-use: Context7 for FastAPI security docs + Sequential Thinking for auth flow + IDE diagnostics after implementation
```

**Database Operations:**
```
User: "Optimize MySQL queries for transaction sync"
→ Auto-use: Context7 for MySQL docs + Sequential Thinking for optimization strategy + IDE execution for testing
```

**Error Resolution:**
```
User: "Fix TypeScript errors in Vue components"
→ Auto-use: IDE diagnostics first + Context7 for Vue/TS docs + Sequential Thinking if complex fix needed
```

### Performance Guidelines
- Batch Context7 calls when multiple libraries are involved
- Use Sequential Thinking for planning before implementation
- Run IDE diagnostics after any code changes
- Always prefer current Context7 docs over built-in knowledge for external libraries

### Current Date Context (Critical for Research)

**Current Date: July 2025**
- AI training cutoff: 2024
- **Always account for 2025 context** when researching libraries, frameworks, or APIs
- Use Context7 and WebSearch for **current 2025 documentation and versions**
- When searching, include "2025" in queries for latest information
- Be aware that built-in knowledge may be outdated for recent developments