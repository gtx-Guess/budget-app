import { defineStore } from 'pinia';
import { ref } from 'vue';
import { User } from "@/types/aliases";

export const useLocalStore = defineStore('localStore', () => {
    //vars
    const user = ref<User | {}>({});


    //setters
    const setUser = (user_dict: User) => {
        user.value = user_dict;
    };

    return {
        user,
        setUser
    };
});