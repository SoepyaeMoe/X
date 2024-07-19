<template>
    <MainView>
        <div class="blog-main-container">
            <button class=" btn btn-primary" id="back-btn" @click="back">&#129080;Back</button>
            <div class="blog-detail">
                <div class="form-group">
                    <label for="category">Category</label>
                    <input v-model="category" class="form-control" list="categories" name="category" type="text"
                        id="category" placeholder="Category">
                    <datalist id="categories">
                        <option v-for="category in categories" :key="category.id" :value="category.name">
                            <!-- {{ category.name }} -->
                        </option>
                    </datalist>
                </div>
                <div class="form-group mt-1 mb-1">
                    <label for="title">Title</label>
                    <input v-model="title" type="text" id="title" class="form-control" placeholder="Content title">
                </div>

                <img class="blog-img" v-if="blog_image != '/images/blogs/default_blog_image.png'"
                    :src="$url + blog_image" alt="" id="image">
                <div class="form-group mt-1">
                    <label for="image">Image</label>
                    <input @change="selectFile($event)" type="file" class="form-control" id="image">
                </div>

                <div class="form-group mt-1">
                    <label for="content">Content</label>
                    <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" id="content"></ckeditor>
                </div>

                <button @click="create" class="btn btn-primary mt-1 float-right">UPDATE</button>
            </div>
        </div>
    </MainView>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue';
import MainView from './MainView.vue';
import { mapGetters } from 'vuex';
import { ClassicEditor, Bold, Essentials, Italic, Mention, FindAndReplace, Paragraph, Undo, Code, Font, Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine } from 'ckeditor5';
export default {
    components: {
        MainView,
        ckeditor: CKEditor.component,
    },
    data() {
        return {
            editorData: '',
            editor: ClassicEditor,
            editorConfig: {
                plugins: [
                    Bold, Essentials, Italic, Mention, Paragraph, Undo, Font, Code,
                    Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine, FindAndReplace
                ],
                toolbar: [
                    'undo', 'redo', '|', 'findAndReplace', 'bold', 'italic', 'link', 'code', 'codeBlock', 'fontSize',
                    'fontFamily', 'fontColor', 'fontBackgroundColor', 'horizontalLine', 'bulletedList',
                    'numberedList', 'alignment'
                ],
            },

            category: '',
            title: '',
            blog_id: null,
            blog_image: null,
            selectedFile: null,
        };
    },
    computed: {
        ...mapGetters(['categories', 'blog_detail'])
    },
    methods: {
        // ...mapActions(['createBlog', 'getBlogDetail']),
        selectFile(e) {
            this.selectedFile = e.target.files[0]
            const previewImg = document.getElementById('image')

            if (this.selectedFile) {
                const reader = new FileReader()
                reader.readAsDataURL(this.selectedFile)
                reader.onload = e => {
                    previewImg.src = e.target.result
                }
            }
        },
        create() {
            let data = {
                'category': this.category,
                'title': this.title,
                'content': this.editorData,
                'image': this.selectedFile
            }
            this.$axios.put(`update-blog/${this.blog_id}/`, data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                if (response.data.status == 200) {
                    this.$router.push({ name: 'blog-detail', params: this.blog_id })
                }

                if (response.data.status == 400) {
                    document.querySelector("#login-form").style.display = 'flex';
                    document.querySelector("#register-form").style.display = 'none';
                }
            })
        },
        back() {
            window.history.back()
        },
    },
    mounted() {
        this.$axios.get(`blogs/${this.$route.params.id}`).then(response => {
            if (response.data.status == 200) {
                this.blog_id = response.data.data.id
                this.category = response.data.data.category.name
                this.title = response.data.data.title
                this.editorData = response.data.data.content
                this.blog_image = response.data.data.image
            }
        })
    },
}
</script>

<style lang="scss" scoped></style>