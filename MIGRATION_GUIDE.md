# **Budget App Windows Migration Guide**

Follow these steps exactly to migrate your Budget App to the Windows machine and configure it properly.

## **Step 1: Get Windows Machine IP Address**

First, find the Windows machine's IP address:
```bash
ipconfig
```
Look for the IPv4 address (example: `192.168.0.150`). **Write this down - you'll need it for the next steps.**

## **Step 2: Update Environment Variables**

Replace `YOUR_WINDOWS_IP` with the actual IP address you found in Step 1.

### **File 1: `budget-vue/.env`**
```
VITE_BACKEND_URL=http://YOUR_WINDOWS_IP:8000
```

### **File 2: `docker-compose.yml` (around line 10)**
Find this line:
```yaml
- VITE_BACKEND_URL=http://192.168.0.209:8000
```
Change to:
```yaml
- VITE_BACKEND_URL=http://YOUR_WINDOWS_IP:8000
```

### **File 3: `budget-backend/.env` (line 2)**
Find this line:
```
ALLOWED_ORIGIN=http://localhost:5173,http://192.168.0.209:5173,https://app.tdnet.xyz
```
Change to:
```
ALLOWED_ORIGIN=http://localhost:5173,http://YOUR_WINDOWS_IP:5173,https://app.tdnet.xyz
```

## **Step 3: Start Docker Services**

```bash
docker-compose up --build
```

Wait for all services to start (database, backend, frontend, phpmyadmin).

## **Step 4: Create Demo User and Data**

Run these commands in order:

```bash
# Create the demo user account
cd budget-backend
python scripts/create_demo_user.py

# Generate demo bank accounts and transactions  
python scripts/generate_demo_data.py
```

You should see output like:
- ✅ Demo user created successfully!
- ✅ Generated 3 demo accounts
- ✅ Generated 1000 demo transactions

## **Step 5: Update Kemp Load Balancer**

In your Kemp configuration:

1. **Find the "app" SubVS real server**
2. **Change the IP address** from `192.168.0.209` to `YOUR_WINDOWS_IP`
3. **Keep the port as `5173`**
4. **Save the configuration**

## **Step 6: Test Everything**

### **Local Access:**
- Frontend: `http://YOUR_WINDOWS_IP:5173`
- Backend: `http://YOUR_WINDOWS_IP:8000`

### **Login Credentials:**
- **Real User**: `tiko` / (your existing password)
- **Demo User**: `demo` / `demo123`

### **External Access:**
- `https://app.tdnet.xyz` (should work once Kemp is updated)

## **Step 7: Verify Demo Data**

Login as the demo user and verify:
- ✅ 3 bank accounts appear (Chase, Bank of America, Wells Fargo)
- ✅ ~1000 transactions over 6 months
- ✅ Realistic account balances
- ✅ All app features work (clickable accounts, transactions, etc.)

## **Troubleshooting**

If something doesn't work:

1. **Check Docker logs:**
   ```bash
   docker logs budgetapp-frontend-1
   docker logs budgetapp-backend-1
   ```

2. **Verify IP replacement:** Make sure all 3 files have the correct Windows IP

3. **Test locally first:** Ensure `http://YOUR_WINDOWS_IP:5173` works before testing external access

4. **Check Kemp:** Ensure the real server shows as "Up" in Kemp interface

## **Success Criteria**

✅ Docker containers running  
✅ Demo user created  
✅ Demo data generated  
✅ Local access works  
✅ Kemp updated  
✅ External access via `app.tdnet.xyz` works  

---

**Note:** Replace `YOUR_WINDOWS_IP` with the actual IP address from Step 1 in ALL the files above.