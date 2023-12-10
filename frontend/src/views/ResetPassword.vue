<script setup>
import NavBar from '/src/components/NavBar.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { tokenRequest } from '../services/api/auth'

const router = useRouter()

const email = ref('')
const errors = ref('')

const submitForm = async () => {
    try {
        await tokenRequest.post('/api/v1/users/reset_password/', {
            email: email.value,
        })
        router.push({
            name: 'Login',
        })
    } catch (error) {
        errors.value = error.response.data
    }
}
</script>

<template>
    <NavBar />
    <div>
        <div>
            <h2>Reset your password</h2>
        </div>

        <div>
            <ul v-if="errors" style="color: rgb(214, 16, 16)">
                <li v-for="(value, index) in errors" :key="index">
                    {{ index.charAt(0).toUpperCase() + index.slice(1) }} : {{ value }}
                </li>
            </ul>
            <form @submit.prevent="submitForm">
                <div>
                    <label for="email">Email address</label>
                    <div>
                        <input
                            id="email"
                            v-model="email"
                            name="email"
                            type="email"
                            autocomplete="email"
                            required=""
                        />
                    </div>
                </div>

                <div>
                    <button type="submit">Reset password</button>
                </div>
            </form>
            <p><button @click="$router.back()">Go back</button></p>
        </div>
    </div>
</template>
