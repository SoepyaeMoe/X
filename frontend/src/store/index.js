import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    auth_user: null,
    user_info: null,
    blogs: [],
    top_blogs: [],
    categories: [],
    blog_detail: {},
    blog_loading: true,
    v_error: [],
  },
  getters: {
    auth_user(state) {
      return state.auth_user
    },
    user_info(state) {
      return state.user_info
    },
    blog_loading(state) {
      return state.blog_loading
    },
    blogs(state) {
      return state.blogs
    },
    categories(state) {
      return state.categories
    },
    all_categories(state) {
      return state.categories
    },
    blog_detail(state) {
      return state.blog_detail
    },
    top_blogs(state) {
      return state.top_blogs
    },
    heart_count(state) {
      let heart_count = 0;
      for (let i = 0; i < state.blogs.length; i++) {
        heart_count += state.blogs[i].hearts.length
      }
      return heart_count;
    },
    v_error(state) {
      return state.v_error
    }
  },
  mutations: {
    setAuthUser(state, payload) {
      state.auth_user = payload
    },
    setUserInfo(state, payload) {
      state.user_info = payload
    },
    setBlogs(state, payload) {
      state.blogs = payload
      state.blog_loading = false
    },
    setCategory(state, payload) {
      state.categories = payload
    },
    setBlogDetail(state, payload) {
      state.blog_detail = payload
    },
    setTopBlogs(state, payload) {
      state.top_blogs = payload
    },
    updateReactStatus(state, data) {
      if (data.event != 'only_one') {
        for (let i = 0; i < state.blogs.length; i++) {
          if (state.blogs[i].id == data.blog) {
            if (state.blogs[i].hearts.length != 0) {
              state.blogs[i].hearts.forEach(h => {
                if (h.user == data.user) {
                  state.blogs[i].hearts = state.blogs[i].hearts.filter(h => {
                    return h.user != data.user
                  })
                } else {
                  state.blogs[i].hearts.push({ 'blog': data.blog, 'user': data.user })
                }
              })
            } else {
              state.blogs[i].hearts.push({ 'blog': data.blog, 'user': data.user })
            }
          }
        }
      }

      if (data.event == 'only_one') {
        if (state.blog_detail.hearts.length != 0) {
          state.blog_detail.hearts.forEach(e => {
            if (e.user == data.user) {
              state.blog_detail.hearts = state.blog_detail.hearts.filter(h => {
                return h.user != data.user
              })
            } else {
              state.blog_detail.hearts.push({ 'blog': data.blog, 'user': data.user })
            }
          })
        } else {
          state.blog_detail.hearts.push({ 'blog': data.blog, 'user': data.user })
        }
      }
    },
    setError(state, payload) {
      state.v_error = payload
    }
  },
  actions: {
    getAuthUser({ commit }) {
      axios.get('auth-user/').then(response => {
        if (response.data.status == 200) {
          commit('setAuthUser', response.data.data)
        }
        if (response.data.status == 400) {
          commit('setAuthUser', null)
        }
      })
    },
    updateAuthUser({ commit }, data) {
      axios.put('auth-user/', data, { headers: { 'Content-Type': 'multipart/form-data' } }).then(response => {
        if (response.data.status == 200) {
          commit('setAuthUser', response.data.data)
        }
        if (response.data.status == 400) {
          commit('setError', response.data.data)
        }
      })
    },
    userProfileInfo({ commit }, id) {
      axios.get(`profile/${id}/`).then(response => {
        if (response.data.status == 200) {
          commit('setUserInfo', response.data.data)
        }

        if (response.data.status == 400) {
          commit('setUserInfo', null)
        }
      })
    },
    getCategories({ commit }) {
      axios.get(`category/`).then((response) => {
        if (response.status == 200) {
          if (response.status == 200) {
            commit('setCategory', response.data.data)
          }
        }
      })
    },
    getBlogs({ commit }, data) {
      axios.get(`blogs/?page=${data.page}&query=${data.query}`).then((response) => {
        commit('setBlogs', response.data.results)
      })
    },
    getUserOfBlogs({ commit }, data) {
      axios.get(`blogs/?page=${data.page}&query=${data.query}&id=${data.user_id}`).then((response) => {
        commit('setBlogs', response.data.results)
      })
    },
    getBlogDetail({ commit }, id) {
      axios.get(`blogs/${id}`).then(response => {
        if (response.data.status == 200) {
          commit('setBlogDetail', response.data.data)
        }
      })
    },
    getTopBlogs({ commit }) {
      axios.get('top-blogs/').then(response => {
        if (response.data.status == 200) {
          commit('setTopBlogs', response.data.data)
        }
      })
    },
    reactToBlog({ commit }, data) {
      commit('updateReactStatus', {
        'blog': data.blog, 'user': data.user, 'event': data.event
      })
      axios.post(`heart-blog/${data.blog}/`)
    },
  },
  modules: {}
})
