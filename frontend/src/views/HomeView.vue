<template>
    <MainView>
        <!-- blog container -->
        <div class="blog-main-container">
            <div v-if="blogs.length == 0 & !blog_loading" class="no-results">
                <img src="@/assets/image/no-results.png" alt="">
                <h3>No Results Found</h3>
                <p>Check your search criteria or try different keywords</p>
            </div>
            <div class="blog-container">
                <div class="blog" v-for="(blog, index) in blogs" :key="index">
                    <img class="blog-img" :src="$url + blog.image" alt="">

                    <h3 class="title">
                        <router-link :to="{ name: 'blog-detail', params: { id: blog.id } }">
                            {{ blog.title.substring(0, 25) }}...
                        </router-link>
                    </h3>

                    <div class="content" v-html="blog.content">
                    </div>
                    <div class="author-info">
                        <img class="author-img" :src="$url + blog.author.image" alt="">
                        <router-link :to="{ name: 'profile', params: { id: blog.author.id } }">
                            {{ blog.author.name }}
                        </router-link>
                        <small>{{ $filter.formatDate(blog.created_at) }}</small>
                    </div>
                    <div class="heart text-center">
                        <img v-if="!auth_user" src="@/assets/image/heart_default.svg" alt="">
                        <img @click="react(blog.id)" v-if="auth_user && !checkReact(blog.hearts)"
                            src="@/assets/image/heart_outline.svg" alt="">
                        <img @click="react(blog.id)" v-if="auth_user && checkReact(blog.hearts)"
                            src="@/assets/image/heart.svg" alt="">
                        <small>{{ blog.hearts.length }}</small>
                    </div>
                </div>

                <LoadingPlaceholder v-if="blog_loading" />
            </div>
            <button class="btn btn-primary d-none">Load More...</button>
        </div>
        <!-- end blog container -->
    </MainView>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import MainView from './MainView.vue'
import LoadingPlaceholder from '@/components/LoadingPlaceholder.vue'
export default {
    components: {
        MainView, LoadingPlaceholder
    },
    data() {
        return {
            page: 1,
        }
    },
    computed: {
        ...mapGetters(['blogs', 'blog_loading', 'auth_user']),
    },
    methods: {
        ...mapActions(['getBlogs', 'reactToBlog']),
        checkReact(heartList) {
            for (let i = 0; i < heartList.length; i++) {
                if (heartList[i].user == this.auth_user.id) {
                    return true
                }
            }
            return false
        },
        react(id) {
            this.reactToBlog({ 'blog': id, 'user': this.auth_user.id })
        },
    },
    mounted() {
        this.$root.is_in_profile = false;
        this.getBlogs({ query: '', page: this.page })
    }
}
</script>

<style></style>