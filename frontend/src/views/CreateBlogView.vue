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
                <div class="form-group mt-1">
                    <label for="title">Title</label>
                    <input v-model="title" type="text" id="title" class="form-control" placeholder="Content title">
                </div>
                <div class="form-group mt-1">
                    <label for="content">Content</label>
                    <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" id="content"></ckeditor>
                </div>
                <div class="form-group mt-1 mb-1">
                    <label for="image">Image</label>
                    <input @change="selectFile($event)" type="file" class="form-control" id="image">
                </div>
                <img src="" class="blog-img" alt="" id="preview">
                <button @click="create" class="btn btn-primary">Create</button>
            </div>
        </div>
    </MainView>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue';
import MainView from './MainView.vue';
import { mapActions, mapGetters } from 'vuex';
import { ClassicEditor, Bold, Essentials, Italic, Mention, Paragraph, Undo, Code, Font, Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine } from 'ckeditor5';
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
                    Link, AutoLink, List, Alignment, CodeBlock, HorizontalLine
                ],
                toolbar: [
                    'undo', 'redo', '|', 'bold', 'italic', 'link', 'code', 'codeBlock', 'fontSize',
                    'fontFamily', 'fontColor', 'fontBackgroundColor', 'horizontalLine', 'bulletedList',
                    'numberedList', 'alignment'
                ],
            },

            category: '',
            title: '',
            selectedFile: null,
        };
    },
    computed: {
        ...mapGetters(['categories'])
    },
    methods: {
        ...mapActions(['createBlog']),
        selectFile(e) {
            this.selectedFile = e.target.files[0]
            const previewImg = document.getElementById('preview')
            if (this.selectedFile) {
                const reader = new FileReader()
                reader.readAsDataURL(this.selectedFile)
                reader.onload = function (e) {
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
            this.$axios.post('create-blog/', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                if (response.data.status == 200) {
                    this.$router.push({ name: 'home' })
                }
            })
        },
        back() {
            window.history.back()
        },
    },
}
</script>

<style lang="scss" scoped></style>