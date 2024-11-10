<template>
    <router-link to="/">Home</router-link>
    <main class="login-main">
        <div class="outer-box">
            <div class="login-box">
                <section>
                    <input maxlength="40" type="text" placeholder="User/Email Address" v-model="userName">
                    <input maxlength="20" type="text" placeholder="Password" v-model="password">
                </section>
                <section style="height: 80px;">
                    <button @click="login()">Login</button>
                    <button>Create Account</button>
                </section>
            </div>
        </div>
    </main>
</template>

<script lang="ts" setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { LoginApiResponse } from '@/types/aliases';

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const userName = ref('');
const password = ref('');

const login = async () => {
    if(userName.value && password.value){
        try {
            const resp = await axios.post(`${BASE_URL}/login`, {
                'user': userName.value,
                'password': password.value
            }, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            await handleResp(resp).then(() => {
                // userName.value = '';
                // password.value = '';
            });      
        } catch (error) {
            console.log(error);
        }
    }else{
        alert('User and password have to be included!!');
    };
};

const handleResp = async (resp: LoginApiResponse) => {
    console.log(resp);
    console.log("Authenticated successfully!");
};

</script>

<style scoped>
.login-main {
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 150px;
    width: 100%;
}

.outer-box {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 400px;
    background: rgb(115, 253, 216);
    padding: 10px;
    border-radius: 20px;
    height: 400px;
    box-shadow: 2px 2px 24px rgba(0, 0, 0, 0.3);
}

.login-box {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 200px;
    height: 250px;
}
.login-box > section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    height: 100px;
}

.login-box > section > input,
.login-box > section > button {
    padding: 0;
    text-align: center;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

.login-box > section > button {
    font-size: 20pt;
    width: 240px;
}

.login-box > section > input {
    height: 35px;
    width: 300px;
    font-size: 18pt;
}

</style>