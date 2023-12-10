<script setup>
import NavBar from '/src/components/NavBar.vue'
import { useAuthStore } from '../store'

const authStore = useAuthStore()
</script>

<template>
    <NavBar />
    <div v-if="authStore.user">
        <h1>Profile</h1>
        <p>
            Name: {{ authStore.user.last_name }}
            {{ authStore.user.first_name }}
        </p>
        <p>Email: {{ authStore.user.email }}</p>
    </div>
</template>
