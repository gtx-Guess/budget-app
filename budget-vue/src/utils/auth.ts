import axios from 'axios';
import { useLocalStore } from '@/stores/localStorage';

/**
 * Loads user data and accounts from the backend
 * Used both during login and app initialization
 */
export const loadUserData = async (store = null) => {
    const localStore = store || useLocalStore();
    const { setUser, setAccounts, setTransactions } = localStore;
    
    try {
        // Load user data, accounts, and transactions in parallel
        const [userResponse, accResponse, tranResponse] = await Promise.all([
            axios.get(`/api/get_current_user`),
            axios.get(`/api/get_local_accounts`),
            axios.get(`/api/get_local_transactions`)
        ]);
        
        // Set user data from authenticated endpoint
        setUser({
            first_name: userResponse.data.first_name,
            last_name: userResponse.data.last_name,
            email_address: userResponse.data.email_address
        });
        
        // Set accounts data
        setAccounts({ data: accResponse.data });
        
        // Set transactions data
        setTransactions({ data: tranResponse.data });
        
        console.log('✅ User data and transactions loaded successfully');
        return true;
        
    } catch (error) {
        console.error("Error fetching user data:", error);
        return false;
    }
};

/**
 * Checks if user is authenticated by calling the backend
 */
export const checkAuthentication = async (): Promise<boolean> => {
    try {
        const response = await axios.post('/api/authenticated');
        return response.data.status === 200;
    } catch (error) {
        return false;
    }
};