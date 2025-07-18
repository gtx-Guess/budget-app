import { User, Transactions, Accounts } from "@/types/aliases";
import { defineStore } from 'pinia';
import { ref, watch } from 'vue';


export const useLocalStore = defineStore('localStore', () => {
    //vars
    const user = ref<User | null>(null);
    const transactions = ref<Transactions>({ data: [] });
    const accounts = ref<Accounts>({ data: [] });
    
    // Initialize dark mode from localStorage on store creation
    const initializeDarkModeValue = () => {
        const saved = localStorage.getItem('darkMode');
        if (saved !== null) {
            return JSON.parse(saved);
        } else {
            // Default to system preference
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
    };
    
    const isDarkMode = ref<boolean>(initializeDarkModeValue());

    // Initialize dark mode from localStorage
    const initializeDarkMode = () => {
        const saved = localStorage.getItem('darkMode');
        if (saved !== null) {
            isDarkMode.value = JSON.parse(saved);
        } else {
            // Default to system preference
            isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        applyDarkMode();
    };

    // Apply dark mode class to html element
    const applyDarkMode = () => {
        if (isDarkMode.value) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    };
    
    // Apply dark mode immediately
    applyDarkMode();
    
    // Watch for dark mode changes and persist
    watch(isDarkMode, (newValue) => {
        localStorage.setItem('darkMode', JSON.stringify(newValue));
        applyDarkMode();
    });

    //setters
    const setUser = (user_dict: User) => {
        user.value = user_dict;
    };
    const setTransactions = (transaction_dict: Transactions) => {
        transactions.value = transaction_dict;
    };
    const setAccounts = (accounts_dict: Accounts) => {
        accounts.value = accounts_dict
    };
    const toggleDarkMode = () => {
        isDarkMode.value = !isDarkMode.value;
    };

    return {
        //objects
        accounts,
        transactions,
        user,
        isDarkMode,
        //setters
        setAccounts,
        setTransactions,
        setUser,
        toggleDarkMode,
        initializeDarkMode
    };
});