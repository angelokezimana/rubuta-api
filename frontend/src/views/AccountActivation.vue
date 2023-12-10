<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { activateAccount } from '/src/services/api/auth'

const route = useRoute()

const activationStatus = ref('pending')

onMounted(async () => {
    try {
        const activationUid = route.params.uid
        const activationToken = route.params.token

        await activateAccount(activationUid, activationToken)

        activationStatus.value = 'success'
    } catch (error) {
        activationStatus.value = 'error'
    }
})
</script>
<template>
    <div>
        <div v-if="activationStatus === 'pending'">Activating your account...</div>
        <div v-else-if="activationStatus === 'success'">
            Account activated successfully!
            <router-link :to="{ name: 'Login' }">Log in</router-link>
        </div>
        <div v-else-if="activationStatus === 'error'">
            Error activating account.
            <router-link :to="{ name: 'Home' }">Go to homepage</router-link>
        </div>
    </div>
</template>
