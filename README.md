# Budget Tracker App

I wanted to build a budget app to track my spending. This app connects to my bank accounts using Fintable, which syncs data to Airtable, and then pulls that data into a local database for fast access and offline development.

## Architecture
- **Bank Connection**: Fintable connects to actual bank accounts
- **Data Storage**: Fintable syncs to Airtable (daily + manual refresh)
- **Local Database**: MySQL stores synced transaction and account data
- **Frontend**: Vue.js with real-time data display
- **Backend**: FastAPI with automatic background sync service
- **Smart Data Management**: Automatic cleanup of old Airtable records to stay within free tier limits

## Features
- ✅ User authentication system with JWT tokens
- ✅ Real bank account and transaction data via Fintable → Airtable
- ✅ Automatic daily sync from Airtable to local database
- ✅ Manual sync trigger for immediate data refresh
- ✅ Docker development environment for easy setup
- ✅ Offline development capability with local database
- ✅ Hot reload for both frontend and backend development
- ✅ Intelligent Airtable record cleanup (keeps 4 months, deletes older records automatically)
- ✅ Local database stores complete transaction history permanently
- ✅ Fast local queries while maintaining access to recent data from anywhere

## Smart Data Management
The app automatically manages Airtable's free tier 1,000 record limit by:
- Monitoring record count and triggering cleanup at 80% capacity (800 records)
- Keeping the most recent 4 months of transactions in Airtable for accessibility
- Storing complete historical data permanently in the local database
- Running cleanup automatically during daily syncs

## Working on:
- Data visualization and spending reports
- Budget setting and tracking features
- Transaction categorization and analysis
- Enhanced UI/UX improvements

## Tech Stack
- **Frontend**: Vue 3, TypeScript, Vite, Pinia
- **Backend**: FastAPI, Python, PyMySQL
- **Database**: MySQL
- **External APIs**: Fintable, Airtable
- **Development**: Docker, Docker Compose

## Getting Started
1. Clone the repository
2. Set up environment variables:
   - **Backend**: Create `budget-backend/.env` with Airtable credentials and database config
   - **Frontend**: Create `budget-vue/.env` with `VITE_BACKEND_URL=http://localhost:8000`
3. Run `docker-compose up --build`
4. Access the app at http://localhost:5173

## Development URLs
- **Main App**: http://localhost:5173 (Vue.js frontend)
- **API**: http://localhost:8000 (FastAPI backend)  
- **Database**: http://localhost:8080 (phpMyAdmin interface)

This setup gives me real financial data while maintaining complete control over the data flow and storage, all while staying within free tier limits and keeping costs minimal.