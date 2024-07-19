<template>
    <!-- login form -->
    <div class="auth-form-container" id="login-form">
        <span class="close-btn" id="close-btn">&times;</span>
        <form @submit.prevent="login" class="auth-form">
            <h3 class="text-center color-primary">Login Here</h3>
            <p v-if="$root.message" class="color-success text-center">{{ $root.message }}</p>
            <div class="form-group">
                <label for="l_email">Email</label>
                <input v-model="email" @keyup="changing('email')" class="form-control"
                    :class="{ 'border-danger': hasEmailError }" type="email" id="l_email" placeholder="Enter your email"
                    required>
                <small class="color-danger">{{ emailError }}</small>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" @keyup="changing('password')" class="form-control"
                    :class="{ 'border-danger': hasPasswordError }" type="password" id="password"
                    placeholder="Enter your password" required>
                <small class="color-danger">{{ passwordError }}</small>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
            <p class="text-center">Don't have an account? <span
                    class="color-primary register-btn cursor-pointer">Register</span></p>
        </form>
    </div>
    <!-- end login form -->
</template>

<script>
export default {
    name: 'app',
    data() {
        return {
            email: '',
            password: '',

            emailError: '',
            passwordError: '',
            hasEmailError: false,
            hasPasswordError: false,
        }
    },
    methods: {
        login() {
            this.$axios.post('login/', {
                email: this.email,
                password: this.password
            }).then(response => {
                if (response.data.status == 400) {
                    if (response.data.data['email']) {
                        this.emailError = response.data.data['email'][0]
                        this.hasEmailError = true
                    }
                    if (response.data.data['password']) {
                        this.passwordError = response.data.data['password'][0]
                        this.hasPasswordError = true
                    }
                }
                if (response.data.status == 200) {
                    const assetToken = response.data.data.access
                    const refreshToken = response.data.data.refresh
                    localStorage.setItem('assetToken', assetToken)
                    localStorage.setItem('refreshToken', refreshToken)
                    this.$store.commit('setAuthUser', response.data.user)

                    window.location.reload()
                    // document.querySelector('#login-form').style.display = 'none'
                }
            })
        },
        changing(field) {
            if (field == 'email') {
                this.emailError = ''
                this.hasEmailError = false
            }
            if (field == 'password') {
                this.passwordError = ''
                this.hasPasswordError = false
            }
        }
    },
}
</script>

<style></style>