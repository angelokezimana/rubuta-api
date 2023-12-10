<script setup>
import NavBar from '/src/components/NavBar.vue'
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '../store'

const authStore = useAuthStore()

const form = ref({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    re_password: '',
})

onMounted(() => {
    authStore.authErrors = []
})

watch(
    () => authStore.errors,
    (newStateValue, oldStateValue) => {
        form.value.password = ''
        form.value.re_password = ''
    }
)
</script>
<template>
    <NavBar />
    <div>
        <div>
            <h2>Create your account</h2>
        </div>

        <div>
            <ul v-if="authStore.errors.non_field_errors" style="color: rgb(214, 16, 16)">
                <li v-for="(value, index) in authStore.errors.non_field_errors" :key="index">
                    {{ value }}
                </li>
            </ul>
            <form @submit.prevent="authStore.register(form)">
                <div>
                    <label for="first_name">First name</label>
                    <div>
                        <input
                            id="first_name"
                            v-model="form.first_name"
                            name="first_name"
                            type="text"
                            autocomplete="given-name"
                            required=""
                        />
                    </div>
                        <ul
                            v-if="authStore.errors.first_name"
                            style="color: rgb(214, 16, 16)"
                        >
                            <li
                                v-for="(value, index) in authStore.errors.first_name"
                                :key="index"
                            >
                                {{ value }}
                            </li>
                        </ul>
                </div>

                <div>
                    <label for="last_name">Last name</label>
                    <div>
                        <input
                            id="last_name"
                            v-model="form.last_name"
                            name="last_name"
                            type="text"
                            autocomplete="family-name"
                            required=""
                        />
                    </div>
                    <ul
                            v-if="authStore.errors.last_name"
                            style="color: rgb(214, 16, 16)"
                        >
                            <li
                                v-for="(value, index) in authStore.errors.last_name"
                                :key="index"
                            >
                                {{ value }}
                            </li>
                        </ul>
                </div>

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
                    <label for="password">Password</label>
                    <div>
                        <input
                            id="password"
                            v-model="form.password"
                            name="password"
                            type="password"
                            autocomplete="new-password"
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
                    <label for="re_password">Confirm Password</label>
                    <div>
                        <input
                            id="re_password"
                            v-model="form.re_password"
                            name="re_password"
                            type="password"
                            autocomplete="new-password"
                            required=""
                        />
                    </div>
                </div>

                <div>
                    <button type="submit">Sign Up</button>
                </div>
            </form>
            <p>
                Do you have an account?
                {{ ' ' }}

                <router-link :to="{ name: 'Login' }">Log in</router-link>
            </p>
        </div>
    </div>
</template>
