import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'ckeditor5/ckeditor5.css';
import './assets/css/global.css'
import './assets/css/style.css'
import './assets/js/script.js'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000/'
const assetToken = localStorage.getItem('assetToken')
if (assetToken) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${assetToken}`
}

axios.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('assetToken');
            localStorage.removeItem('refreshToken')
            axios.defaults.headers.common['Authorization'] = 'Bearer';
            window.location.reload()
        }
        return Promise.reject(error);
    }
);

let app = createApp(App)
app.config.globalProperties.$filter = {
    formatDate(dateString) {
        if (dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US',
                {
                    year: 'numeric', month: 'short', day: 'numeric',
                    hour: 'numeric', minute: 'numeric'
                });
        }
        return '';
    }
}
app.config.globalProperties.$axios = axios
app.config.globalProperties.$url = 'http://localhost:8000/'
app.use(store)
app.use(router)
app.mount('#app')
