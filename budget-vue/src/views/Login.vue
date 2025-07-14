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
import { handleMessage, message, showMessage } from '../utils/utils';
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';

import AlertBubble from '@/components/AlertBubble.vue';
import axios from 'axios';



const userName = ref('');
const password = ref('');

const route = useRouter();

const login = async () => {
    if(userName.value && password.value){
        try {
            await axios.post(`/api/login`, {
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
    min-height: 100vh;
    background: var(--bg-primary);
    transition: background-color 0.3s ease;
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
    background: var(--bg-tertiary-ov);
    box-shadow: 2px 2px 24px rgba(107, 155, 79, 0.3);
    border: 2px solid rgb(107, 155, 79);
    transition: background-color 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

html.dark .outer-box {
    background: var(--bg-secondary);
    box-shadow: 2px 2px 24px rgba(139, 185, 111, 0.3);
    border: 2px solid rgb(139, 185, 111);
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
    gap: 15px;
}

.login-box > section > input {
    padding: 10px;
    text-align: center;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border-light);
    background: var(--bg-secondary);
    color: var(--text-primary);
    transition: all 0.3s ease;
    height: 35px;
    width: 300px;
    font-size: 18pt;
}

html.dark .login-box > section > input {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-light);
    box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
}

.login-box > section > button {
    padding: 10px;
    text-align: center;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    border: 1px solid rgb(107, 155, 79);
    background: rgb(154 178 145) !important;
    color: #ffffff !important;
    transition: all 0.3s ease;
    font-size: 20pt;
    width: 240px;
    cursor: pointer;
    font-weight: 600;
}

.login-box > section > button:hover {
    background: rgb(85, 125, 62) !important;
    transform: translateY(-2px);
}

html.dark .login-box > section > button {
    background: rgb(95 114 83) !important;
    color: #ffffff !important;
    border: 1px solid rgb(139, 185, 111);
    box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
}

html.dark .login-box > section > button:hover {
    background: rgb(120, 165, 95) !important;
}


.login-box > section > input:focus {
    outline: none;
    border-color: rgb(107, 155, 79);
    box-shadow: 0 0 0 2px rgba(107, 155, 79, 0.3);
}

html.dark .login-box > section > input:focus {
    border-color: rgb(139, 185, 111);
    box-shadow: 0 0 0 2px rgba(139, 185, 111, 0.3);
}

.login-box > section > input::placeholder {
    color: var(--text-secondary);
}

html.dark .login-box > section > input::placeholder {
    color: var(--text-secondary);
}

</style>