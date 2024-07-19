<template>
  <router-view />
</template>

<script>
// import Nav from './components/Nav.vue'
export default {
  name: 'App',
  data() {
    return {
      is_in_profile: false,
      message: null,
      error_message: null,
      page: 1,
      user_id: null,
    }
  },
}
</script>
<style></style>
