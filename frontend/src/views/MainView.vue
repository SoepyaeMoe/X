<template>
  <Nav />

  <div class="container main-container">

    <SideBar />
    <slot />

    <Login />
    <SingUp />
  </div>
</template>

<script>
import { initializeAuthForm } from '@/assets/js/script'
import Nav from '@/components/Nav.vue'
import SideBar from '@/components/SideBar.vue'
import Login from '@/components/Login.vue'
import SingUp from '@/components/SignUp.vue'
import { mapActions } from 'vuex'

export default {
  name: 'HomeView',
  components: {
    Nav, SideBar, Login, SingUp
  },
  methods: {
    ...mapActions(['getAuthUser'])
  },
  mounted() {
    initializeAuthForm();
    this.getAuthUser()
  },
}
</script>
