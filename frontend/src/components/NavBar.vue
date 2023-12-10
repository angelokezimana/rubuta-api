<script setup>
import { useAuthStore } from '/src/store'

const authStore = useAuthStore()
</script>
<template>
    <nav>
        <div>
            <router-link :to="{ name: 'Home' }">SAS</router-link>
        </div>

        <div v-if="authStore.user">
            <ul>
                <!-- New Message link -->
                <li>
                    <router-link to="/profile">New Message</router-link>
                </li>
                <!-- Inbox link -->
                <li>
                    <router-link to="/profile">Inbox</router-link>
                </li>
                <!-- Sent link -->
                <li>
                    <router-link to="/profile">Sent</router-link>
                </li>
                <!-- Sent link -->
                <li>
                    <router-link to="/profile">Draft</router-link>
                </li>
                <!-- Sent link -->
                <li>
                    <router-link to="/profile">Bin</router-link>
                </li>
            </ul>
            <span>
                Hello {{ authStore.user.last_name }} |
                <router-link :to="{ name: 'Profile' }">Profile</router-link>
                |
                <button type="button" @click="authStore.logout">Logout</button>
            </span>
        </div>
        <div v-else>
            <router-link :to="{ name: 'Login' }">Log in</router-link>
            |
            <router-link :to="{ name: 'SignUp' }">Sign up</router-link>
        </div>
    </nav>
</template>
