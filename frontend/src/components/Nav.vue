<template>
    <!-- nav -->
    <nav>
        <div class="logo">
            <router-link :to="{ name: 'home' }">
                <img id="nav_logo" src="@/assets/image/X_logo_2023_original.svg" alt="">
            </router-link>
        </div>
        <!-- auth -->
        <div v-if="!auth_user" class="auth_button">
            <button class="btn btn-outline login-btn" id="login-btn">Log in</button>
            <button class="btn btn-primary register-btn" id="register-btn">Sign up</button>
        </div>
        <!-- end auth -->

        <!-- profile info -->
        <div v-if="auth_user" class="profile-info cursor-pointer" @click="isClose = !isClose">
            <img :src="$url + auth_user.image" alt="">
            <div>
                <p class="username">{{ auth_user.name }}</p>
                <small class="email">{{ auth_user.email }}</small>
            </div>
        </div>
        <!-- end profile info -->

        <div v-if="auth_user" class="drop-down shadow" :class="{ 'd-none': isClose }">
            <div class="item">
                <router-link :to="{ name: 'profile', params: { id: auth_user.id } }"
                    class="cursor-pointer">Profile</router-link>
            </div>
            <div class="item cursor-pointer" @click="logout">Logout</div>
        </div>

    </nav>

    <!-- mobile top nav -->
    <div class="mobile-nav" id="mobile-nav">
        <div class="logo">
            <router-link :to="{ name: 'home' }">
                <img id="nav_logo" src="@/assets/image/X_logo_2023_original.svg" alt="">
            </router-link>
        </div>
        <div class="search_box">
            <input @keyup.enter="filterBlogs(query, '')" type="text" placeholder="Search..." v-model="query">
            <img @click="filterBlogs(query, '')" src="../assets/image/search.svg" alt="">
        </div>
    </div>
    <!-- end mobile top nav -->

    <!-- mobile bottom nav -->
    <div>
        <div class="mobile-bottom-nav">
            <ul>
                <li class="cursor-pointer">
                    <router-link :to="{ name: 'home' }"><img src="@/assets/image/home.svg" alt=""></router-link>
                </li>
                <li class="cursor-pointer"><img src="@/assets/image/filter.svg" alt=""></li>
                <li class="cursor-pointer" v-if="auth_user">
                    <router-link :to="{ name: 'create-blog' }"><img src="@/assets/image/add.svg" alt=""></router-link>
                </li>
                <li class="cursor-pointer" v-if="auth_user"><img src="@/assets/image/notification.svg" alt=""></li>
                <li class="cursor-pointer" v-if="auth_user">
                    <router-link :to="{ name: 'profile', params: { id: auth_user.id } }">
                        <img src="@/assets/image/profile.svg" alt="">
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
    <!-- env mobile bottom nav -->
    <!-- end nav -->
</template>

<script>
import Swal from 'sweetalert2'
import { mapActions, mapGetters } from 'vuex'
export default {
    name: 'app',
    data() {
        return {
            query: '',
            isClose: true,
            page: 1,
        }
    },
    computed: {
        ...mapGetters(['auth_user'])
    },
    methods: {
        ...mapActions(['getBlogs']),
        filterBlogs(query, event) {
            if (event.type == 'click') {
                let category = document.querySelectorAll('.category')
                category.forEach(e => {
                    e.classList.remove('category-active')
                })
                event.target.classList.add('category-active')
            }
            this.$store.state.blog_loading = true
            this.getBlogs({ query: query, page: this.page })
        },
        logout() {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: "btn btn-primary m-1",
                    cancelButton: "btn btn-danger"
                },
                buttonsStyling: false
            });
            swalWithBootstrapButtons.fire({
                title: "Are you sure?",
                text: "You want to logout.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Yes, Logout!",
                cancelButtonText: "No, cancel!",
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.$axios.post('logout/', { refresh_token: localStorage.getItem('refreshToken') }).then(response => {

                        if (response.data.status == 200) {
                            localStorage.removeItem('assetToken')
                            localStorage.removeItem('refreshToken')
                            swalWithBootstrapButtons.fire({
                                text: "Logout success.",
                                icon: "success"
                            }).then(result => {
                                if (result.isConfirmed) {
                                    this.$router.push({ name: 'home' }).then(() => {
                                        window.location.reload()
                                    })
                                }
                            })
                        }

                        if (response.data.status == 400) {
                            Swal.fire({
                                icon: "error",
                                title: "Oops...",
                                text: "Something went wrong!",
                            });
                        }
                    })
                } else if (
                    result.dismiss === Swal.DismissReason.cancel
                ) {
                    swalWithBootstrapButtons.fire({
                        title: "Cancelled",
                        icon: "error"
                    });
                }
            });
        }
    },
}
</script>

<style></style>