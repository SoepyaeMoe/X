<template>
    <MainView>
        <div class="blog-main-container">
            <div v-if="user_info" class="profile-header">
                <div class="cover-img">
                    <img src="@/assets/image/cover_photo.jpg" alt="">
                </div>
                <div class="profile-img">
                    <img :src="$url + user_info.image" alt="">
                </div>
                <div class="user-info">
                    <h3>{{ user_info.name }}</h3>
                    <p>{{ user_info.bio }} </p>
                    <div class="info-badge-container">
                        <div class="info-badge">
                            <span>Blogs {{ blogs.length }}</span>
                        </div>
                        <div class="info-badge">
                            <span>Hearts {{ heart_count }}</span>
                        </div>
                    </div>
                </div>
                <router-link :to="{ name: 'profile-setting', params: { id: auth_user.id } }"
                    v-if="auth_user && auth_user.id == user_info.id" class="setting-icon">
                    <img src="@/assets/image/setting.svg" alt="">
                </router-link>
            </div>
            <div class="profile-body">
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
                            <p>{{ blog.author.name }}</p>
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
        </div>
    </MainView>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import MainView from './MainView.vue';
import LoadingPlaceholder from '@/components/LoadingPlaceholder.vue';
export default {
    components: {
        MainView, LoadingPlaceholder
    },
    data() {
        return {
            page: 1
        }
    },
    computed: {
        ...mapGetters(['auth_user', 'blogs', 'user_info', 'blog_loading', 'heart_count']),
    },
    methods: {
        ...mapActions(['getUserOfBlogs', 'reactToBlog', 'userProfileInfo']),
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
        this.$root.is_in_profile = true;
        this.$root.user_id = this.$route.params.id;
        this.getUserOfBlogs({ query: '', page: this.page, user_id: this.$route.params.id });
        this.userProfileInfo(this.$route.params.id);
    },
}
</script>

<style lang="scss" scoped></style>