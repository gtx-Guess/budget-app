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
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { handleMessage, message, showMessage } from '../utils/utils';
import AlertBubble from '@/components/AlertBubble.vue';

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

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
        const resp = await axios.post(`${BASE_URL}/api/create_user`, user, {
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
}

.create-box > section > input,
.create-box > section > button {
    padding: 0;
    text-align: center;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

.create-box > section > button {
    font-size: 20pt;
    width: 240px;
}

.create-box > section > input {
    height: 35px;
    width: 300px;
    font-size: 18pt;
}

</style>