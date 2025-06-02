import { User, Transactions, Accounts } from "@/types/aliases";
import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';


export const useLocalStore = defineStore('localStore', () => {
    //vars
    const user = ref<User | null>(null);
    const transactions = ref<Transactions>({ data: [] });
    const accounts = ref<Accounts>({ data: [] });
    const vendorCategories = ref<string[]>([]);

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
    const setCategories = (category_list: string[]) => {
        vendorCategories.value = category_list
    };

    const getCategories = async () => {
        try {
            const resp = await axios.get(`/api/get_vendor_categories`);
            setCategories(resp.data);
        } catch (error) {
            console.log(error);
        }
    };

    return {
        //objects
        accounts,
        transactions,
        vendorCategories,
        user,
        //setters
        setAccounts,
        setTransactions,
        setCategories,
        setUser,
        //getters
        getCategories
    };
});