import { defineStore } from 'pinia';
import { ref } from 'vue';
import { User, Transactions, Accounts } from "@/types/aliases";

export const useLocalStore = defineStore('localStore', () => {
    //vars
    const user = ref<User | null>(null);
    const transactions = ref<Transactions>({ data: [] });
    const accounts = ref<Accounts>({ data: [] });

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

    return {
        //objects
        accounts,
        transactions,
        user,
        //setters
        setAccounts,
        setTransactions,
        setUser
    };
});