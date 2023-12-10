<script setup>
import NavBar from '/src/components/NavBar.vue'
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '../store'

const form = ref({
    email: '',
    password: '',
})
const authStore = useAuthStore()

onMounted(() => {
    authStore.authErrors = []
})

watch(
    () => authStore.errors,
    (newStateValue, oldStateValue) => {
        form.value.password = ''
    }
)
</script>

<template>
    <NavBar />
    <div>
        <div>
            <h2>Sign in to your account</h2>
        </div>

        <div>
            <div v-if="authStore.errors.detail" style="color: rgb(214, 16, 16)">
                {{ authStore.errors.detail }}
            </div>
            <div
                v-if="authStore.status"
                style="background-color: rgb(16, 214, 42); color: white"
            >
                {{ authStore.status }}
            </div>
            <form @submit.prevent="authStore.login(form)">
                <div>
                    <label for="email">Email address</label>
                    <div>
                        <input
                            id="email"
                            v-model="form.email"
                            name="email"
                            type="email"
                            autocomplete="email"
                            required=""
                        />
                    </div>
                    <ul
                        v-if="authStore.errors.email"
                        style="color: rgb(214, 16, 16)"
                    >
                        <li
                            v-for="(value, index) in authStore.errors.email"
                            :key="index"
                        >
                            {{ value }}
                        </li>
                    </ul>
                </div>

                <div>
                    <div>
                        <label for="password">Password</label>
                        <div>
                            <router-link :to="{ name: 'ResetPassword' }"
                                >Forgot password?</router-link
                            >
                        </div>
                    </div>
                    <div>
                        <input
                            id="password"
                            v-model="form.password"
                            name="password"
                            type="password"
                            autocomplete="current-password"
                            required=""
                        />
                    </div>
                    <ul
                        v-if="authStore.errors.password"
                        style="color: rgb(214, 16, 16)"
                    >
                        <li
                            v-for="(value, index) in authStore.errors.password"
                            :key="index"
                        >
                            {{ value }}
                        </li>
                    </ul>
                </div>

                <div>
                    <button type="submit">Login</button>
                </div>
            </form>
            <p>
                Don't have an account yet?
                {{ ' ' }}

                <router-link :to="{ name: 'SignUp' }">Sign up</router-link>
            </p>
        </div>
    </div>
</template>
