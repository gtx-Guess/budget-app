import axios from 'axios';
import { useLocalStore } from '@/stores/localStorage';

/**
 * Loads user data and accounts from the backend
 * Used both during login and app initialization
 */
export const loadUserData = async () => {
    const localStore = useLocalStore();
    const { setUser, setAccounts } = localStore;
    
    try {
        // Load both user data and accounts in parallel
        const [userResponse, accResponse] = await Promise.all([
            axios.get(`/api/get_current_user`),
            axios.get(`/api/get_local_accounts`)
        ]);
        
        // Set user data from authenticated endpoint
        setUser({
            first_name: userResponse.data.first_name,
            last_name: userResponse.data.last_name,
            email_address: userResponse.data.email_address
        });
        
        // Set accounts data
        setAccounts({ data: accResponse.data });
        
        console.log('✅ User data loaded successfully');
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