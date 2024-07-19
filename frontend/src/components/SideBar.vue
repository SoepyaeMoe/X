<template>
    <!-- sidebar -->
    <div class="sidebar-container">
        <div class="sidebar">
            <div class="search_box">
                <input @keyup.enter="filterBlogs(query, '')" type="text" placeholder="Search blogs..." v-model="query">
                <img class="cursor-pointer" src="../assets/image/search.svg" alt="" @click="filterBlogs(query, '')">
            </div>
            <router-link v-if="auth_user" :to="{ name: 'create-blog' }" class="btn btn-primary mt-1 add-btn">
                <img src="@/assets/image/add-button-svgrepo-com.svg" alt="">
                Create Blog
            </router-link>
            <div class="categories card shadow">
                <h2>Categories</h2>
                <ul>
                    <li class="category category-active" @click="filterBlogs('', $event)">All</li>
                    <li class="category" v-for="(category, index) in categories.slice(0, len_of_cate)" :key="index"
                        @click="filterBlogs(category.name, $event)">
                        {{ category.name }}
                    </li>
                    <p class="text-center cursor-pointer" v-if="categories.length > 6 && len_of_cate == 6"
                        @click="len_of_cate = categories.length">see more... </p>
                    <p class="text-center cursor-pointer" v-if="categories.length > 6 && len_of_cate > 6"
                        @click="len_of_cate = 6">see less... </p>
                </ul>
            </div>
            <!-- top posts -->
            <div class=" top-posts card shadow">
                <h2>Top Posts</h2>
                <div class="top-post" v-for="(top_blogs, index) in top_blogs" :key="index">
                    <h1>{{ index + 1 }}</h1>
                    <div>
                        <router-link :to="{ name: 'blog-detail', params: { id: top_blogs.id } }">
                            <h3>{{ top_blogs.title.substring(0, 25) }}</h3>
                        </router-link>
                        <p v-html="top_blogs.content.substring(0, 70) + '...'"></p>
                    </div>
                </div>
            </div>
            <!-- end top posts -->
        </div>
    </div>
    <!-- end sidebar -->
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    data() {
        return {
            query: '',
            len_of_cate: 6,
        }
    },
    computed: {
        ...mapGetters(['categories', 'top_blogs', 'auth_user'])
    },
    methods: {
        ...mapActions(['getCategories', 'getBlogs', 'getTopBlogs', 'getUserOfBlogs']),
        filterBlogs(query, event) {
            if (event.type == 'click') {
                let category = document.querySelectorAll('.category')
                category.forEach(e => {
                    e.classList.remove('category-active')
                })
                event.target.classList.add('category-active')
            }
            this.$store.state.blog_loading = true
            let data = { query: query, page: this.$root.page, user_id: this.$root.user_id }
            if (this.$root.is_in_profile) {
                this.getUserOfBlogs(data)
            } else {
                this.getBlogs(data)
            }
        }
    },
    mounted() {
        this.getCategories()
        this.getTopBlogs()
    },
}
</script>

<style></style>