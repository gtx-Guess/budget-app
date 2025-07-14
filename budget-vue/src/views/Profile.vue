<template>
    <div class="profile flex flex-col">
        <AlertBubble :alertText="alertMessage" :visible="showAlert" />
        <section class="profile-header flex justify-between items-center">
            <h2 class="text-matcha-400 font-semibold">Profile</h2>
        </section>
        
        <div class="content-container">
            <!-- User Information and Connected Accounts Grid -->
            <div class="user-accounts-grid">
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
                        Loading user information...
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
                                    No accounts connected yet. Use the Dashboard to sync your accounts.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Account Settings Section -->
            <div class="profile-section bg-matcha-light rounded-lg">
                <h3 class="section-title text-matcha-400 font-semibold">Account Settings</h3>
                <div class="settings-grid">
                    <!-- Password Change -->
                    <div class="password-form">
                        <h4 class="form-subtitle text-matcha-400 font-medium">Change Password</h4>
                        <div class="input-group">
                            <label class="text-matcha-700">Current Password</label>
                            <input 
                                type="password" 
                                v-model="currentPassword"
                                placeholder="Enter current password"
                                class="settings-input"
                            />
                        </div>
                        <div class="input-group">
                            <label class="text-matcha-700">New Password</label>
                            <input 
                                type="password" 
                                v-model="newPassword"
                                placeholder="Enter new password"
                                class="settings-input"
                            />
                        </div>
                        <div class="input-group">
                            <label class="text-matcha-700">Confirm New Password</label>
                            <input 
                                type="password" 
                                v-model="confirmPassword"
                                placeholder="Confirm new password"
                                class="settings-input"
                            />
                        </div>
                        <div class="button-container">
                            <button 
                                @click="updatePassword"
                                :disabled="!canUpdatePassword"
                                class="update-btn"
                                :class="{ 'disabled': !canUpdatePassword }"
                            >
                                {{ isUpdatingPassword ? 'Updating...' : 'Update Password' }}
                            </button>
                        </div>
                    </div>
                    
                    <!-- Email Change -->
                    <div class="email-form">
                        <h4 class="form-subtitle text-matcha-400 font-medium">Change Email Address</h4>
                        <div class="input-group">
                            <label class="text-matcha-700">Current Email</label>
                            <input 
                                type="email" 
                                :value="user?.email_address || ''"
                                disabled
                                placeholder="Current email address"
                                class="settings-input disabled"
                            />
                        </div>
                        <div class="input-group">
                            <label class="text-matcha-700">New Email Address</label>
                            <input 
                                type="email" 
                                v-model="newEmail"
                                placeholder="Enter new email address"
                                class="settings-input"
                            />
                        </div>
                        <div class="input-group">
                            <label class="text-matcha-700">Confirm New Email</label>
                            <input 
                                type="email" 
                                v-model="confirmEmail"
                                placeholder="Confirm new email address"
                                class="settings-input"
                            />
                        </div>
                        <div class="button-container">
                            <button 
                                @click="updateEmail"
                                :disabled="!canUpdateEmail"
                                class="update-btn"
                                :class="{ 'disabled': !canUpdateEmail }"
                            >
                                {{ isUpdatingEmail ? 'Updating...' : 'Update Email' }}
                            </button>
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
import { ref, computed, onMounted } from 'vue';
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import AlertBubble from '@/components/AlertBubble.vue';

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { user, accounts, isDarkMode } = storeToRefs(localStore);
const { setUser, toggleDarkMode } = localStore;

// Password change form data
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isUpdatingPassword = ref(false);

// Email change form data
const newEmail = ref('');
const confirmEmail = ref('');
const isUpdatingEmail = ref(false);

// Alert functionality
const alertMessage = ref('');
const showAlert = ref(false);

// Local backup of accounts count to prevent disappearing
const localAccountsCount = ref(0);

// Initialize local account count from store if available
if (accounts.value?.data?.length) {
    localAccountsCount.value = accounts.value.data.length;
}

// Get connected accounts count
const connectedAccountsCount = computed(() => {
    const storeCount = accounts.value?.data?.length || 0;
    return storeCount > 0 ? storeCount : localAccountsCount.value;
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

// Password validation
const canUpdatePassword = computed(() => {
    return currentPassword.value.length > 0 && 
           newPassword.value.length >= 6 && 
           confirmPassword.value === newPassword.value &&
           !isUpdatingPassword.value;
});

// Email validation
const canUpdateEmail = computed(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return newEmail.value.length > 0 && 
           emailRegex.test(newEmail.value) &&
           confirmEmail.value === newEmail.value &&
           newEmail.value !== user.value?.email_address &&
           !isUpdatingEmail.value;
});

// Show alert function
const showAlertMessage = (message: string, duration: number = 3000) => {
    alertMessage.value = message;
    showAlert.value = true;
    
    setTimeout(() => {
        showAlert.value = false;
    }, duration);
};

// Update password function
const updatePassword = async () => {
    if (!canUpdatePassword.value) return;
    
    isUpdatingPassword.value = true;
    
    try {
        const response = await axios.post('/api/update_password', {
            current_password: currentPassword.value,
            new_password: newPassword.value
        });
        
        // Success
        showAlertMessage(response.data.message || 'Password updated successfully!');
        
        // Clear form
        currentPassword.value = '';
        newPassword.value = '';
        confirmPassword.value = '';
        
    } catch (error) {
        console.error('Password update error:', error);
        let errorMessage = 'Failed to update password';
        if (axios.isAxiosError(error)) {
            errorMessage = error.response?.data?.detail || error.message;
        }
        showAlertMessage(errorMessage);
    } finally {
        isUpdatingPassword.value = false;
    }
};

// Update email function
const updateEmail = async () => {
    if (!canUpdateEmail.value) return;
    
    isUpdatingEmail.value = true;
    
    try {
        const response = await axios.post('/api/update_email', {
            new_email: newEmail.value
        });
        
        // Success
        showAlertMessage(response.data.message || 'Email updated successfully!');
        
        // Update user data in store
        if (user.value) {
            setUser({
                ...user.value,
                email_address: newEmail.value
            });
        }
        
        // Clear form
        newEmail.value = '';
        confirmEmail.value = '';
        
    } catch (error) {
        console.error('Email update error:', error);
        let errorMessage = 'Failed to update email';
        if (axios.isAxiosError(error)) {
            errorMessage = error.response?.data?.detail || error.message;
        }
        showAlertMessage(errorMessage);
    } finally {
        isUpdatingEmail.value = false;
    }
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

/* User Information and Connected Accounts Grid */
.user-accounts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 0;
}

@media (max-width: 768px) {
    .user-accounts-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
}

/* User Information Section */
.user-info-section,
.account-summary-section,
.settings-section,
.profile-section {
    padding: 20px;
}

.user-info-section h3,
.account-summary-section h3,
.settings-section h3,
.profile-section h3 {
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
    color: white !important;
    background-color: rgb(107, 155, 79) !important;
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
    .settings-section,
    .profile-section {
        padding: 15px;
    }
    
    .count-circle {
        width: 50px;
        height: 50px;
        font-size: 20px;
    }
}

/* Account Settings Section */
.settings-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    width: 100%;
}

@media (max-width: 768px) {
    .settings-grid {
        grid-template-columns: 1fr;
        gap: 40px;
    }
}

.password-form,
.email-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-subtitle {
    margin: 0 0 15px 0;
    font-size: 16px;
    border-bottom: 1px solid rgba(107, 155, 79, 0.2);
    padding-bottom: 8px;
}

html.dark .form-subtitle {
    border-bottom-color: rgba(139, 185, 111, 0.2);
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-group label {
    font-size: 14px;
    font-weight: 500;
}

.settings-input {
    padding: 12px;
    border: 2px solid rgba(107, 155, 79, 0.2);
    border-radius: 8px;
    background: white;
    color: var(--text-primary);
    font-size: 14px;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 300px;
}

.settings-input:focus {
    outline: none;
    border-color: rgb(107, 155, 79);
    box-shadow: 0 0 0 3px rgba(107, 155, 79, 0.1);
}

.settings-input.disabled {
    background-color: rgba(107, 155, 79, 0.1);
    color: rgba(107, 155, 79, 0.7);
    cursor: not-allowed;
}

html.dark .settings-input {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border-color: rgba(139, 185, 111, 0.2);
}

html.dark .settings-input:focus {
    border-color: rgb(139, 185, 111);
    box-shadow: 0 0 0 3px rgba(139, 185, 111, 0.1);
}

html.dark .settings-input.disabled {
    background-color: rgba(139, 185, 111, 0.1);
    color: rgba(139, 185, 111, 0.7);
}

.button-container {
    margin-top: 10px;
    margin-bottom: 10px;
}

.update-btn {
    padding: 12px 24px;
    background: rgb(107, 155, 79);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 200px;
}

.update-btn:hover:not(.disabled) {
    background: rgb(85, 125, 62);
    transform: translateY(-1px);
}

.update-btn.disabled {
    background: rgba(107, 155, 79, 0.5);
    cursor: not-allowed;
    transform: none;
}

html.dark .update-btn {
    background: rgb(139, 185, 111);
}

html.dark .update-btn:hover:not(.disabled) {
    background: rgb(120, 165, 95);
}

html.dark .update-btn.disabled {
    background: rgba(139, 185, 111, 0.5);
}

</style>