import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '/src/views/HomePage.vue'
import { useAuthStore } from '../store'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('/src/views/LoginPage.vue'),
        meta: {
            requiresGuest: true,
        },
    },
    {
        path: '/sign-up',
        name: 'SignUp',
        component: () => import('/src/views/SignUp.vue'),
        meta: {
            requiresGuest: true,
        },
    },
    {
        path: '/activate/:uid/:token',
        name: 'ActivateAccount',
        component: () => import('/src/views/AccountActivation.vue'),
        meta: {
            requiresGuest: true,
        },
    },
    {
        path: '/reset-password',
        name: 'ResetPassword',
        component: () => import('/src/views/ResetPassword.vue'),
        meta: {
            requiresGuest: true,
        },
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('/src/views/UserProfile.vue'),
        meta: {
            requiresAuth: true,
        },
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.user) {
        return { name: 'Login', query: { redirect: to.fullPath } }
    }

    if (to.meta.requiresGuest && authStore.user) {
        return { name: 'Home' }
    }
})

export default router
