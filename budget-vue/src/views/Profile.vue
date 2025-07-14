<template>
    <div class="profile flex flex-col">
        <section class="profile-header flex justify-between items-center">
            <h2 class="text-matcha-400 font-semibold">Profile</h2>
            <button @click="loadUserData" class="sync-button bg-matcha-400 text-white rounded-sm cursor-pointer transition-opacity hover-opacity">Refresh Data</button>
        </section>
        
        <div class="content-container">
            <!-- User Information Section -->
            <div class="user-info-section bg-matcha-light rounded-lg">
                <h3 class="text-matcha-400 font-semibold">User Information</h3>
                <div v-if="user" class="user-details">
                    <div class="user-detail-row">
                        <span class="detail-label text-matcha-700">Full Name:</span>
                        <span class="detail-value font-medium text-matcha-400">
                            {{ user.first_name }} {{ user.last_name }}
                        </span>
                    </div>
                    <div class="user-detail-row">
                        <span class="detail-label text-matcha-700">Email Address:</span>
                        <span class="detail-value font-medium text-matcha-400">
                            {{ user.email_address }}
                        </span>
                    </div>
                    <div class="user-detail-row">
                        <span class="detail-label text-matcha-700">User Name:</span>
                        <span class="detail-value font-medium text-matcha-400">
                            {{ getUserDisplayName() }}
                        </span>
                    </div>
                </div>
                <div v-else class="no-user-data text-matcha-700 text-center">
                    No user information available. Click "Refresh Data" to load your profile.
                </div>
            </div>
            
            <!-- Account Summary Section -->
            <div class="account-summary-section bg-matcha-light rounded-lg">
                <h3 class="text-matcha-400 font-semibold">Connected Accounts</h3>
                <div class="account-summary-content">
                    <div class="account-count-display">
                        <div class="count-circle bg-matcha-400 text-white">
                            {{ connectedAccountsCount }}
                        </div>
                        <div class="count-details">
                            <div class="count-label text-matcha-700">
                                {{ connectedAccountsCount === 1 ? 'Bank Account' : 'Bank Accounts' }} Connected
                            </div>
                            <div v-if="connectedAccountsCount === 0" class="no-accounts-message text-matcha-700">
                                No accounts connected yet. Visit the Dashboard to sync your accounts.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Settings Section -->
            <div class="settings-section bg-matcha-light rounded-lg">
                <h3 class="text-matcha-400 font-semibold">Settings</h3>
                <div class="settings-content">
                    <!-- Dark Mode Toggle -->
                    <div class="setting-item">
                        <div class="setting-info">
                            <div class="setting-title text-matcha-400 font-medium">Dark Mode</div>
                            <div class="setting-description text-matcha-700">
                                Switch between light and dark themes
                            </div>
                        </div>
                        <div class="toggle-container" @click="toggleDarkMode">
                            <div class="toggle-label" :class="{ 'active': isDarkMode }">
                                <span class="toggle-slider" :class="{ 'checked': isDarkMode }"></span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Future settings placeholder -->
                    <div class="coming-soon-notice text-matcha-700 text-center">
                        More settings coming soon...
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { user, accounts, isDarkMode } = storeToRefs(localStore);
const { setUser, setAccounts, toggleDarkMode } = localStore;

// Load user and account data
const loadUserData = async () => {
    try {
        // Load both user data and accounts in parallel
        const [userResponse, accResponse] = await Promise.all([
            axios.get(`/api/get_current_user`),
            axios.get(`/api/get_local_accounts`)
        ]);
        
        // Set user data from authenticated endpoint
        setUser({
            first_name: userResponse.data.first_name,
            last_name: userResponse.data.last_name,
            email_address: userResponse.data.email_address
        });
        
        // Set accounts data
        setAccounts({ data: accResponse.data });
        
    } catch (error) {
        console.error("Error fetching user data:", error);
        // If there's an auth error, the axios interceptor will handle redirect to login
    }
};

// Get connected accounts count
const connectedAccountsCount = computed(() => {
    return accounts.value?.data?.length || 0;
});

// Get user display name (username from email or full name)
const getUserDisplayName = () => {
    if (!user.value) return '';
    
    // Extract username from email (part before @)
    if (user.value.email_address) {
        return user.value.email_address.split('@')[0];
    }
    
    // Fallback to first name
    return user.value.first_name || 'User';
};

</script>

<style scoped>
.profile-header {
    margin: 20px 0;
}

.profile-header h2 {
    margin: 0;
    font-size: 38px;
}

.sync-button {
    border: none;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
}

.content-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    margin-bottom: 60px;
}

/* User Information Section */
.user-info-section,
.account-summary-section,
.settings-section {
    padding: 20px;
}

.user-info-section h3,
.account-summary-section h3,
.settings-section h3 {
    margin: 0 0 20px 0;
    font-size: 18px;
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-width: 600px;
    margin: 0 auto;
}

.user-detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 16px;
    border-bottom: 1px solid rgba(107, 155, 79, 0.1);
    background: rgba(107, 155, 79, 0.02);
    border-radius: 6px;
    margin-bottom: 4px;
}

.user-detail-row:last-child {
    border-bottom: 1px solid rgba(107, 155, 79, 0.1);
    margin-bottom: 0;
}

.detail-label {
    font-size: 14px;
    min-width: 120px;
    font-weight: 500;
}

.detail-value {
    font-size: 14px;
    text-align: right;
    flex: 1;
}

.no-user-data {
    padding: 40px 20px;
    font-style: italic;
}

/* Account Summary Section */
.account-summary-content {
    display: flex;
    justify-content: center;
}

.account-count-display {
    display: flex;
    align-items: center;
    gap: 20px;
}

.count-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    flex-shrink: 0;
}

.count-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.count-label {
    font-size: 16px;
    font-weight: 500;
}

.account-list {
    font-size: 14px;
    line-height: 1.4;
}

.no-accounts-message {
    font-size: 14px;
    font-style: italic;
}

/* Settings Section */
.settings-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid rgba(107, 155, 79, 0.1);
}

.setting-item:last-child {
    border-bottom: none;
}

.setting-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
}

.setting-title {
    font-size: 16px;
}

.setting-description {
    font-size: 13px;
    line-height: 1.4;
}

/* Toggle Switch Styles */
.toggle-container {
    position: relative;
    cursor: pointer;
}

.toggle-label {
    display: inline-block;
    width: 50px;
    height: 26px;
    background-color: #e5e7eb;
    border-radius: 13px;
    position: relative;
    transition: background-color 0.3s ease;
}

.toggle-label.active {
    background-color: rgb(107 155 79);
}

html.dark .toggle-label {
    background-color: #374151;
}

html.dark .toggle-label.active {
    background-color: rgb(139, 185, 111);
}

.toggle-slider {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 22px;
    height: 22px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toggle-slider.checked {
    transform: translateX(24px);
}

.coming-soon-notice {
    padding: 20px;
    font-style: italic;
    border-top: 1px solid rgba(107, 155, 79, 0.1);
    margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .profile-header h2 {
        font-size: 28px;
    }
    
    .user-details {
        max-width: 100%;
        margin: 0;
    }
    
    .user-detail-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        padding: 12px 16px;
    }
    
    .detail-value {
        text-align: left;
    }
    
    .account-count-display {
        flex-direction: column;
        text-align: center;
        gap: 15px;
    }
    
    .setting-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }
    
    .toggle-container {
        align-self: flex-end;
    }
}

@media (max-width: 480px) {
    .user-info-section,
    .account-summary-section,
    .settings-section {
        padding: 15px;
    }
    
    .count-circle {
        width: 50px;
        height: 50px;
        font-size: 20px;
    }
}
</style>