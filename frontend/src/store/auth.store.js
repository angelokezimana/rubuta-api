import { defineStore } from 'pinia'
import {
    registerUser,
    loginUser,
    getUser,
    logoutUser,
    ACCESS_TOKEN,
    REFRESH_TOKEN,
} from '/src/services/api/auth'

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        authUser: JSON.parse(window.localStorage.getItem('user')),
        authErrors: [],
        authStatus: null,
    }),
    getters: {
        user: (state) => state.authUser,
        errors: (state) => state.authErrors,
        status: (state) => state.authStatus,
    },
    actions: {
        async login(data) {
            this.authErrors = []
            try {
                await loginUser(data.email, data.password)

                /**
                 * Use this when we don't want to reload the page
                 * await this.getUser()
                 */
                await this.getUser()
                this.router.push({ name: 'Profile' })
                /**
                 * Use this to reload the page
                 * .then(() => {
                 *      this.router.go()
                 * })
                 */
            } catch (error) {
                this.authErrors = error.response.data
            }
        },
        async register(data) {
            this.authErrors = []
            try {
                await registerUser(
                    data.first_name,
                    data.last_name,
                    data.email,
                    data.password,
                    data.re_password
                )
                this.authStatus =
                    'An email has been sent to your email address containing an activation link. \
                    Please click on the link to activate your account. \
                    If you do not click the link your account will remain inactive and you will not receive further emails. \
                    If you do not receive the email within a few minutes, please check your spam folder.'
                this.router.push({ name: 'Login' })
            } catch (error) {
                this.authErrors = error.response.data
            }
        },
        async getUser() {
            const user = await getUser()
            // update pinia state
            this.authUser = user.data
            // store user details in local storage to keep user logged in between page refreshes
            window.localStorage.setItem('user', JSON.stringify(user.data))
        },
        async logout() {
            this.authUser = null
            window.localStorage.removeItem('user')
            await logoutUser()
            this.router.push({ name: 'Home' })
        },
    },
})
