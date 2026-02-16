# Budget Tracker App

I wanted to build a budget app to track my spending. This app connects to my bank accounts using Fintable, which syncs data to Airtable, and then pulls that data into a local database for fast access and offline development.

## Architecture
- **Bank Connection**: Fintable connects to actual bank accounts
- **Data Storage**: Fintable syncs to Airtable (daily + manual refresh)
- **Local Database**: MySQL stores synced transaction and account data
- **Frontend**: Vue.js with real-time data display and responsive design
- **Backend**: FastAPI with automatic background sync service
- **Smart Data Management**: Automatic cleanup of old Airtable records to stay within free tier limits

## Features

### 🔐 Authentication & Security
- ✅ User authentication system with JWT tokens
- ✅ Automatic token refresh with axios interceptors
- ✅ HttpOnly cookies for secure token storage
- ✅ Protected routes with authentication guards
- ✅ Multi-user support with user-specific data isolation

### 💳 Data Management
- ✅ Real bank account and transaction data via Fintable → Airtable
- ✅ Automatic daily sync from Airtable to local database
- ✅ Manual sync trigger for immediate data refresh
- ✅ Intelligent Airtable record cleanup (keeps 4 months, deletes older records automatically)
- ✅ Local database stores complete transaction history permanently
- ✅ Fast local queries while maintaining access to recent data from anywhere
- ✅ Proper database relationships (users ↔ accounts ↔ transactions)

### 📊 Dashboard & Analytics
- ✅ **Overview Tab**: Account summaries with real-time balance display
- ✅ **Quick Analysis Tab**: 
  - Monthly spending, income, and net change analytics
  - Transaction count and average daily spending
  - Largest expenses and most frequent vendors
  - Spending trends comparing current vs previous month
  - Visual progress bars and interactive charts
  - Account-specific filtering with loading states
- ✅ **Recent Activity Tab**: Latest transactions across all accounts
- ✅ Responsive dashboard controller with mobile-friendly design

### 💰 Transaction Management
- ✅ **Transactions Page**: Comprehensive transaction viewing
- ✅ Account-based filtering with dropdown selection
- ✅ Pagination system (25 transactions per page)
- ✅ Smooth scroll-to-top functionality
- ✅ Full transaction details with vendor, date, amount, and notes
- ✅ Color-coded amounts (green for income, red for expenses)
- ✅ Responsive transaction cards

### 👤 User Profile & Settings
- ✅ **Profile Page**: User information display
- ✅ Connected accounts count
- ✅ Working dark mode toggle with localStorage persistence
- ✅ Real authentication integration

### 🎨 Design & User Experience
- ✅ **Matcha Green Theme**: Consistent color scheme throughout
- ✅ **Full Dark Mode Support**: 
  - System preference detection
  - Manual toggle functionality
  - Smooth transitions between themes
  - Dark mode styling for all components
- ✅ **Responsive Design**: Mobile-first approach with breakpoints
- ✅ **Inter Font**: Clean, modern typography
- ✅ **Utility-First CSS**: Consistent styling with reusable classes
- ✅ **Loading States**: Smooth UX with loading indicators
- ✅ **Visual Enhancements**: Icons, progress bars, and hover effects

### 🔧 Development & Infrastructure
- ✅ Docker development environment for easy setup
- ✅ Offline development capability with local database
- ✅ Hot reload for both frontend and backend development
- ✅ TypeScript support with proper type definitions
- ✅ Pinia state management for reactive data
- ✅ Vue 3 Composition API with `<script setup>` syntax

## Smart Data Management
The app automatically manages Airtable's free tier 1,000 record limit by:
- Monitoring record count and triggering cleanup at 80% capacity (800 records)
- Keeping the most recent 4 months of transactions in Airtable for accessibility
- Storing complete historical data permanently in the local database
- Running cleanup automatically during daily syncs

## Recently Completed:
- ✅ Full dark mode implementation across entire application
- ✅ Enhanced Quick Analysis with spending trends and visual indicators
- ✅ Comprehensive transaction management with pagination
- ✅ User profile system with settings
- ✅ Responsive design improvements
- ✅ Login/signup UI enhancements with proper theming

## Working on:
- Enhanced data visualization and spending reports
- Budget setting and tracking features
- Transaction categorization and analysis
- Performance optimizations

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