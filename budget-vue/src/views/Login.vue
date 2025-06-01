<template>
    <!-- <router-link to="/">Home</router-link> -->
    <main class="login-main">
        <AlertBubble :alertText="message" :visible="showMessage" />
        <div class="outer-box">
            <div class="login-box">
                <section>
                    <input maxlength="40" type="text" placeholder="User/Email Address" v-model="userName">
                    <input maxlength="20" type="password" placeholder="Password" v-model="password">
                </section>
                <section style="height: 80px;">
                    <button @click="login()">Login</button>
                    <button><router-link class="router-link" to="/create">Create Account</router-link></button>
                </section>
            </div>
        </div>
    </main>
</template>

<script lang="ts" setup>
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { handleMessage, message, showMessage } from '../utils/utils';
import AlertBubble from '@/components/AlertBubble.vue';
axios.defaults.withCredentials = true;

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const userName = ref('');
const password = ref('');

const route = useRouter();

const login = async () => {
    if(userName.value && password.value){
        try {
            await axios.post(`${BASE_URL}/api/login`, {
                'user': userName.value,
                'password': password.value
            }, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            handleMessage('Logging in!', route, '/');
        } catch (error) {
            console.log(error);
            handleMessage('Login Unsuccessful, user/password combo failed');
        }
    }else{
        handleMessage('User and password have to be included!');
    };
};

</script>

<style scoped>
.router-link {
    all:unset;
}

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
    padding: 10px;
    border-radius: 20px;
    height: 400px;
    background: rgba(255, 255, 255, 0.16);
    box-shadow: 2px 2px 24px rgb(255, 255, 255);
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