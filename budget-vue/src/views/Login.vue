<template>
    <section style="width: 100%; display: flex; justify-content: center; margin-top: 50px;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><line x1="18" x2="18" y1="20" y2="10"></line><line x1="12" x2="12" y1="20" y2="4"></line><line x1="6" x2="6" y1="20" y2="14"></line></svg>
        <span style="font-weight: bold; font-size: 25pt;">Master of Coin</span>
    </section>
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
import { loadUserData } from '@/utils/auth';

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
            handleMessage('Summoning your ledger ...', route, '/');
            await loadUserData();
        } catch (error) {
            console.log(error);
            handleMessage('The Master of Whisperers reports false credentials.');
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
    align-items: flex-start;
    margin-top: 80px;
    width: 100%;
    min-height: 100vh;
    background: var(--bg-primary);
    transition: background-color 0.3s ease;
    padding: 0 20px;
    box-sizing: border-box;
}

.outer-box {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 400px;
    padding: 10px;
    border-radius: 20px;
    height: 400px;
    background: var(--bg-tertiary-ov);
    box-shadow: 2px 2px 24px rgba(107, 155, 79, 0.3);
    border: 2px solid rgb(107, 155, 79);
    transition: background-color 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    box-sizing: border-box;
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
    width: 260px;
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
    width: 100%;
    max-width: 300px;
    min-width: 200px;
    font-size: 18pt;
    box-sizing: border-box;
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
    width: 100%;
    max-width: 240px;
    min-width: 180px;
    cursor: pointer;
    font-weight: 600;
    box-sizing: border-box;
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

/* Responsive Design */
@media (max-width: 768px) {
    .login-main {
        margin-top: 40px;
        padding: 15px;
    }
    
    .outer-box {
        max-width: 350px;
        height: 380px;
        padding: 15px;
    }
    
    .login-box {
        width: 100%;
        max-width: 250px;
        height: 240px;
    }
    
    .login-box > section > input {
        max-width: 250px;
        font-size: 16pt;
        height: 32px;
    }
    
    .login-box > section > button {
        font-size: 16pt;
        max-width: 200px;
    }
}

@media (max-width: 480px) {
    section span {
        font-size: 20pt !important;
    }
    
    .login-main {
        margin-top: 20px;
        padding: 10px;
    }
    
    .outer-box {
        max-width: 95%;
        height: 360px;
        padding: 10px;
        margin: 0 auto;
    }
    
    .login-box {
        width: 100%;
        max-width: 220px;
        height: 220px;
    }
    
    .login-box > section > input {
        max-width: 220px;
        font-size: 14pt;
        height: 30px;
        padding: 8px;
    }
    
    .login-box > section > button {
        font-size: 14pt;
        max-width: 180px;
        padding: 8px;
    }
}

@media (max-width: 390px) {
    section span {
        font-size: 18pt !important;
    }
    
    .outer-box {
        max-width: 90%;
        height: 340px;
        padding: 8px;
    }
    
    .login-box {
        max-width: 200px;
        height: 200px;
    }
    
    .login-box > section > input {
        max-width: 200px;
        font-size: 13pt;
        height: 28px;
        padding: 6px;
    }
    
    .login-box > section > button {
        font-size: 12pt;
        max-width: 160px;
        padding: 6px;
    }
}

</style>