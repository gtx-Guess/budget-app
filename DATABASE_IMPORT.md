# **Database Import Guide**

This is an alternative to running the demo scripts. Use this if you want to import the complete database with all existing data.

## **Option A: Database Import (Recommended)**

### **Step 1: Copy Database File**
Ensure `budget_app_complete_export.sql` is in your project root directory.

### **Step 2: Start Docker (without running scripts)**
```bash
docker-compose up --build -d
```

Wait 30 seconds for database to initialize.

### **Step 3: Import Database**
```bash
docker exec -i budgetapp-database-1 mysql -u devuser -pdevpassword budget-app < budget_app_complete_export.sql
```

### **Step 4: Verify Import**
```bash
docker exec budgetapp-database-1 mysql -u devuser -pdevpassword budget-app -e "SELECT COUNT(*) as user_count FROM \`budget-app-user\`;"
docker exec budgetapp-database-1 mysql -u devuser -pdevpassword budget-app -e "SELECT COUNT(*) as account_count FROM accounts;"
docker exec budgetapp-database-1 mysql -u devuser -pdevpassword budget-app -e "SELECT COUNT(*) as transaction_count FROM transactions;"
```

You should see:
- **Users**: 2 (Tigran + Demo)
- **Accounts**: Multiple accounts
- **Transactions**: ~1000+ transactions

## **Option B: Fresh Demo Data (Scripts)**

If you prefer to generate fresh demo data, follow the original migration guide steps 4-7.

## **Login Credentials (Both Options)**
- **Real User**: `Tigran` / (your existing password)
- **Demo User**: `demo` / `demo123`