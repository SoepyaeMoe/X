<template>
    <MainView>
        <div v-if="auth_user" class="setting-container blog-main-container">
            <h3>Account</h3>
            <hr class="profile-setting">
            <div class="account-container">
                <div class="account">
                    <div class="label">
                        <label for="name">Name:</label>
                        <label for="email">Email:</label>
                        <label for="profile_pic">Profile Picture:</label>
                        <label for="bio">Bio:</label>
                    </div>
                    <div class="input">
                        <div>
                            <small v-if="v_error.name" class="color-danger d-block">{{ v_error.name }}</small>
                            <input id="name" type="text" v-model="auth_user.name"
                                :class="{ 'v-input-error': v_error.name }" @keyup="$store.state.v_error.name = null">
                        </div>
                        <div>
                            <input id="email" type="email" disabled v-model="auth_user.email">
                        </div>
                        <div class="pp">
                            <input id="profile_pic" type="file" @change="selectFile($event)">
                            <img :src="$url + auth_user.image" alt="" id="pp_image">
                        </div>
                        <div>
                            <textarea id="bio" cols="20" rows="3" v-model="auth_user.bio"></textarea>
                        </div>
                    </div>
                </div>
                <button class="btn btn-primary mt-1" @click="profileInfoChange">Save</button>
                <router-link :to="{ name: 'profile', params: { id: auth_user.id } }"
                    class="btn btn-danger ms-1">Cancle</router-link>
            </div>
            <hr class="profile-setting">
            <h3>Change Password</h3>
            <div class="account-container">
                <div class="account">
                    <div class="label">
                        <span>Old Password:</span>
                        <span>New Password:</span>
                        <span>Confirm Password:</span>
                    </div>
                    <div class="input">
                        <div>
                            <input type="password" v-model="oldPassword"
                                :class="{ 'v-input-error': validation_error.old_password }">
                            <small v-if="validation_error.old_password" class="color-danger d-block">{{
                                validation_error.old_password[0] }}</small>
                        </div>
                        <div>
                            <input type="password" v-model="newPassword"
                                :class="{ 'v-input-error': validation_error.new_password }">
                            <small v-if="validation_error.new_password" class="color-danger d-block">{{
                                validation_error.new_password[0] }}</small>
                        </div>
                        <div>
                            <input type="password" v-model="confirmPassword"
                                :class="{ 'v-input-error': validation_error.confirm_password }">
                            <small v-if="validation_error.confirm_password" class="color-danger d-block">{{
                                validation_error.confirm_password[0] }}</small>
                        </div>
                    </div>
                </div>
                <button class="btn btn-primary mt-1" @click="changePassword">Change</button>
            </div>
            <hr class="profile-setting">
            <h3>Delete all your blogs? </h3>
            <div class="ms-1">
                <div class="alert-warning">
                    <img src="@/assets/image/warning.svg" alt=""><span>If you delete all your blogs, you will lose all
                        of your blogs.</span>
                </div>
                <button class="btn btn-danger" @click="deleteAllBlogs">Delete All Blogs</button>
            </div>
            <hr class="profile-setting">
            <h3>Delete your account?</h3>
            <div class="ms-1">
                <div class="alert-warning">
                    <img src="@/assets/image/warning.svg" alt="">
                    <span>If you delete your account, your account will be deleted permanently and you will not be able
                        to recover your account anymore.</span>
                </div>
                <button class="btn btn-danger" @click="deleteAccount">Delete Account</button>
            </div>
        </div>
    </MainView>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import MainView from './MainView.vue'
import Swal from 'sweetalert2'
export default {
    components: {
        MainView,
    },
    data() {
        return {
            selectedFile: null,
            oldPassword: '',
            newPassword: '',
            confirmPassword: '',
            validation_error: [],   // for password only
        }
    },
    computed: {
        ...mapGetters(['auth_user', 'v_error'])
    },
    methods: {
        ...mapActions(['updateAuthUser', 'changePassword']),
        selectFile(e) {
            this.selectedFile = e.target.files[0]
            const previewImg = document.querySelector('#pp_image');
            if (this.selectFile) {
                const reader = new FileReader()
                reader.readAsDataURL(this.selectedFile)
                reader.onload = e => {
                    previewImg.src = e.target.result
                }
            }
        },
        profileInfoChange() {
            let data = {
                name: this.auth_user.name,
                email: this.auth_user.email,
                bio: this.auth_user.bio,
                image: this.selectedFile
            }
            this.updateAuthUser(data)
        },
        changePassword() {
            this.$axios.post('change-password/', {
                'old_password': this.oldPassword,
                'new_password': this.newPassword,
                'confirm_password': this.confirmPassword,
            }).then(response => {
                if (response.data.status == 200) {

                    this.oldPassword = '';
                    this.newPassword = '';
                    this.confirmPassword = '';
                    this.validation_error = [];

                    const Toast = Swal.mixin({
                        toast: true,
                        position: "top-end",
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                            toast.onmouseenter = Swal.stopTimer;
                            toast.onmouseleave = Swal.resumeTimer;
                        }
                    });
                    Toast.fire({
                        icon: "success",
                        title: response.data.data
                    });
                }
                if (response.data.status == 400) {
                    this.validation_error = response.data.data
                }
            })
        },
        deleteAllBlogs() {
            Swal.fire({
                title: "Are you sure?",
                text: "You won't be able to revert this!",
                icon: "warning",
                showCancelButton: true,
                reverseButtons: true,
                confirmButtonColor: "#ae0000",
                cancelButtonColor: "#007e39",
                confirmButtonText: "Yes, delete it!"
            }).then(async (result) => {
                if (result.isConfirmed) {
                    const { value: password } = await Swal.fire({
                        title: "Enter your password",
                        input: "password",
                        inputLabel: "Password",
                        inputPlaceholder: "Enter your password",
                        customClass: {
                            input: 'text-center'
                        },
                        inputAttributes: {
                            maxlength: "10",
                            autocapitalize: "off",
                            autocorrect: "off"
                        }
                    });
                    if (password) {
                        this.$axios.post('delete-all-blogs/', { 'password': password }).then(response => {
                            if (response.data.status == 200) {
                                Swal.fire({
                                    title: "Deleted!",
                                    text: response.data.data,
                                    icon: "success"
                                });
                            }
                            if (response.data.status == 400) {
                                Swal.fire({
                                    title: "Oops...",
                                    text: response.data.data,
                                    icon: "error"
                                });
                            }
                        })
                    }
                }
            });
        },
        async deleteAccount() {
            const { value: password } = await Swal.fire({
                title: "Enter your password",
                input: "password",
                inputLabel: "Password",
                inputPlaceholder: "Enter your password",
                customClass: {
                    input: 'text-center'
                },
                inputAttributes: {
                    maxlength: "10",
                    autocapitalize: "off",
                    autocorrect: "off"
                }
            });
            if (password) {
                this.$axios.post('delete-account/', { 'password': password }).then(response => {
                    if (response.data.status == 200) {
                        localStorage.removeItem('assetToken')
                        localStorage.removeItem('refreshToken')
                        this.$router.push({ 'name': 'home' }).then(() => window.location.reload())
                    }

                    if (response.data.status == 400) {
                        Swal.fire({
                            title: "Oops...",
                            text: response.data.data,
                            icon: "error"
                        });
                    }
                })
            }
        }
    },
}
</script>
