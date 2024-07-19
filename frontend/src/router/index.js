import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BlogDetailView from '../views/BlogDetailView.vue'
import CreateBlogView from '@/views/CreateBlogView.vue'
import EditBlogView from '@/views/EditBlogView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileSettingView from '@/views/ProfileSettingView.vue'

const routes = [
  { path: '/', component: HomeView, name: 'home' },
  { path: '/blog-detail/:id/', component: BlogDetailView, name: 'blog-detail' },
  { path: '/create-blog/', component: CreateBlogView, name: 'create-blog' },
  { path: '/edit-blog/:id/', component: EditBlogView, name: 'edit-blog' },
  { path: '/profile/:id/', component: ProfileView, name: 'profile' },
  { path: '/profile/:id/setting', component: ProfileSettingView, name: 'profile-setting' },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
