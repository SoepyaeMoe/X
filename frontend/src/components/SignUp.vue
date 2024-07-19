<template>
    <!-- register form --->
    <div class="auth-form-container" id="register-form">
        <span class="close-btn" id="close-btn">&times;</span>
        <form @submit.prevent="signup" action="" class="auth-form">
            <h3 class="text-center color-primary">Sign Up Here</h3>
            <div class="form-group">
                <label for="name">Name</label>
                <input @keyup="changing('name')" v-model="name" class="form-control"
                    :class="{ 'border-danger': hasnameError }" type="text" id="name" placeholder="Enter your name"
                    required>
                <small class="color-danger">{{ nameError }}</small>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input @keyup="changing('email')" v-model="email" class="form-control"
                    :class="{ 'border-danger': hasEmailError }" type="email" id="email" placeholder="Enter your email"
                    required>
                <small class="color-danger">{{ emailError }}</small>
            </div>
            <div class="form-group">
                <label for="password1">Password</label>
                <input @keyup="changing('password1')" v-model="password1" class="form-control"
                    :class="{ 'border-danger': hasPassword1Error }" type="password" name="password1" id="password1"
                    placeholder="Enter your password" required>
                <small class="color-danger">{{ password1Error }}</small>
            </div>
            <div class="form-group">
                <label for="password2">Confirm Password</label>
                <input @keyup="changing('password2')" v-model="password2" class="form-control"
                    :class="{ 'border-danger': haspassword2Error }" type="password" id="password2"
                    placeholder="Confirm your password" required>
                <small class="color-danger">{{ password2Error }}</small>
            </div>

            <button type="submit" class="btn btn-primary">Sign up</button>
            <p class="text-center">Aready have an accound? <span
                    class="color-primary login-btn cursor-pointer">Login</span></p>
        </form>
    </div>
    <!-- end register form -->
</template>

<script>
export default {
    data() {
        return {
            name: null,
            email: null,
            password1: '',
            password2: '',

            nameError: '',
            hasnameError: false,
            emailError: '',
            hasEmailError: false,
            password1Error: '',
            hasPassword1Error: false,
            password2Error: '',
            haspassword2Error: false,
        }
    },
    methods: {
        signup() {
            this.$axios.post('signup/', {
                name: this.name,
                email: this.email,
                password1: this.password1,
                password2: this.password2,
            }).then(response => {
                if (response.data.status == 400) {
                    if (response.data.data['name']) {
                        this.nameError = response.data.data['name'][0]
                        this.hasnameError = true
                    }
                    if (response.data.data['email']) {
                        this.emailError = response.data.data['email'][0]
                        this.hasEmailError = true
                    }
                    if (response.data.data['password1']) {
                        this.password1Error = response.data.data['password1'][0]
                        this.hasPassword1Error = true
                    }
                    if (response.data.data['password2']) {
                        this.password2Error = response.data.data['password2'][0]
                        this.hasPassword2Error = true
                    }
                }

                if (response.data.status == 200) {
                    document.querySelector("#login-form").style.display = 'flex';
                    document.querySelector("#register-form").style.display = 'none';
                    this.$root.message = response.data.message
                }
            })
        },
        changing(field) {
            if (field == 'name') {
                this.nameError = ''
                this.hasnameError = false
            }
            if (field == 'email') {
                this.emailError = ''
                this.hasEmailError = false
            }
            if (field == 'password1') {
                this.password1Error = ''
                this.hasPassword1Error = false
            }
            if (field == 'password2') {
                this.password2Error = ''
                this.hasPassword2Error = false
            }
        }
    },
}
</script>

<style></style>