<template>
    <MainView>
        <div class="blog-main-container">
            <button class="btn btn-primary" id="back-btn" @click="back">&#129080; Back</button>
            <div class="blog-detail" v-if="Object.keys(blog_detail).length !== 0">
                <div class="blog-header">
                    <div class="author-info">
                        <img :src="$url + blog_detail.author.image" alt="">
                        <div>
                            <p class="username">{{ blog_detail.author.name }}</p>
                            <small>{{ $filter.formatDate(blog_detail.created_at) }}</small>
                            <small>{{ blog_detail.view }}</small>
                        </div>
                    </div>
                    <div class="heart">
                        <img v-if="!auth_user" src="@/assets/image/heart_default.svg" alt="">
                        <img @click="react(blog_detail.id)" v-if="auth_user && !checkReact(blog_detail.hearts)"
                            src="@/assets/image/heart_outline.svg" alt="">
                        <img @click="react(blog_detail.id)" v-if="auth_user && checkReact(blog_detail.hearts)"
                            src="@/assets/image/heart.svg" alt="">
                        <small>{{ blog_detail.hearts.length }}</small>
                    </div>
                </div>
                <div v-if="auth_user && auth_user.id == blog_detail.author.id">
                    <div class="edit-icon cursor-pointer shadow" @click="deleteBlog(blog_detail.id)">
                        <img class="" src="@/assets/image/delete.svg" alt="">
                    </div>
                    <router-link class="edit-icon cursor-pointer shadow"
                        :to="{ name: 'edit-blog', param: blog_detail.id }">
                        <img src="@/assets/image/edit.svg" alt="">
                    </router-link>
                </div>
                <h1 class="color-primary">{{ blog_detail.title }}</h1>
                <img class="blog-img" v-if="blog_detail.image != '/images/blogs/default_blog_image.png'"
                    :src="$url + blog_detail.image" alt="">
                <!-- <div class="desc color-primary" v-html="blog_detail.content"></div> -->
                <ckeditor :editor="editor" :disabled="editorDisabled" v-model="blog_detail.content"
                    :config="editorConfig"></ckeditor>
            </div>
        </div>
    </MainView>
</template>

<script>
import MainView from './MainView.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';
import CKEditor from '@ckeditor/ckeditor5-vue';
import { ClassicEditor, Bold, Essentials, Italic, Mention, FindAndReplace, Paragraph, Undo, Code, Font, Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine } from 'ckeditor5';
export default {
    data() {
        return {
            editor: ClassicEditor,
            editorConfig: {
                plugins: [
                    Bold, Essentials, Italic, Mention, Paragraph, Undo, Font, Code,
                    Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine, FindAndReplace
                ],
                toolbar: [
                    'findAndReplace',
                ],
            },
            editorDisabled: true,
        }
    },
    components: {
        MainView,
        ckeditor: CKEditor.component
    },
    methods: {
        ...mapActions(['getBlogDetail', 'reactToBlog']),
        back() {
            window.history.back()
        },
        checkReact(heartList) {
            for (let i = 0; i < heartList.length; i++) {
                if (heartList[i].user == this.auth_user.id) {
                    return true
                }
            }
            return false
        },
        react(id) {
            this.reactToBlog({ 'blog': id, 'user': this.auth_user.id, 'event': 'only_one' })
        },
        deleteBlog(id) {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: "btn btn-primary m-1",
                    cancelButton: "btn btn-danger"
                },
                buttonsStyling: false
            });

            swalWithBootstrapButtons.fire({
                title: "Are you sure?",
                text: "You want to delete this blog.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Yes, Delete it!",
                cancelButtonText: "No, cancel!",
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    this.$axios.delete(`delete-blog/${id}/`).then(response => {
                        if (response.data.status == 200) {
                            swalWithBootstrapButtons.fire({
                                text: "Delete success.",
                                icon: "success"
                            }).then(result => {
                                if (result.isConfirmed) {
                                    this.$router.push({ name: 'home' })
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
                }
                //  else if (
                //     result.dismiss === Swal.DismissReason.cancel
                // ) {
                //     swalWithBootstrapButtons.fire({
                //         title: "Cancelled",
                //         icon: "error"
                //     });
                // }
            });
        }

    },
    computed: {
        ...mapGetters(['blog_detail', 'auth_user']),
    },
    mounted() {
        this.getBlogDetail(this.$route.params.id);
    },
}
</script>

<style lang="scss" scoped></style>