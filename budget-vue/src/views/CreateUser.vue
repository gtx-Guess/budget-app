<template>
    <!-- <router-link to="/">Home</router-link> -->
    <main class="create-main">
        <AlertBubble :alertText="message" :visible="showMessage" />
        <div class="outer-box">
            <div class="create-box">
                <section style="height: 145px;">
                    <input maxlength="15" type="text" placeholder="User Name" v-model="userName">
                    <input maxlength="20" type="text" placeholder="Password" v-model="password">
                    <input maxlength="40" type="text" placeholder="Email Address" v-model="emailAddress">
                </section>
                <section style="height: 85px !important;">
                    <button @click="createAccount">Create Account!</button>
                    <button><router-link class="router-link" to="/login">Login</router-link></button>
                </section>
            </div>
        </div>
    </main>
</template>

<script lang="ts" setup>
import { handleMessage, message, showMessage } from '../utils/utils';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

import AlertBubble from '@/components/AlertBubble.vue';
import axios from 'axios';

const userName = ref('');
const password = ref('');
const emailAddress = ref('');

const router = useRouter();

const createAccount = async () => {
    if(!userName.value || !password.value || !emailAddress){
        handleMessage('All fields have to be filled out!');
        return;
    };
    if(!emailAddress.value.includes('@') || !emailAddress.value.includes('.com')){
        handleMessage('Please enter a valid email address!');
        return;
    }
    const user = {
        user_name: userName.value,
        password: password.value,
        email_address: emailAddress.value
    };

    try {
        const resp = await axios.post(`/api/create_user`, user, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if(resp.status === 200){
            handleMessage(resp.data.message, router,'/login');
        };
    } catch (error) {
        console.log(error);
    };

};

</script>


<style scoped>
.router-link {
    all:unset;
}

.create-main {
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

.create-box {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 200px;
    height: 320px;
}

.create-box > section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    height: 100px;
    gap: 15px;
}

.create-box > section > input {
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

html.dark .create-box > section > input {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-light);
    box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
}

.create-box > section > button {
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

.create-box > section > button:hover {
    background: rgb(85, 125, 62) !important;
    transform: translateY(-2px);
}

html.dark .create-box > section > button {
    background: rgb(95 114 83) !important;
    color: #ffffff !important;
    border: 1px solid rgb(139, 185, 111);
    box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
}

html.dark .create-box > section > button:hover {
    background: rgb(120, 165, 95) !important;
}

.create-box > section > input:focus {
    outline: none;
    border-color: rgb(107, 155, 79);
    box-shadow: 0 0 0 2px rgba(107, 155, 79, 0.3);
}

html.dark .create-box > section > input:focus {
    border-color: rgb(139, 185, 111);
    box-shadow: 0 0 0 2px rgba(139, 185, 111, 0.3);
}

.create-box > section > input::placeholder {
    color: var(--text-secondary);
}

html.dark .create-box > section > input::placeholder {
    color: var(--text-secondary);
}

</style>