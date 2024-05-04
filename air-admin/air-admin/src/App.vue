<template>
  <div id="app">
    <router-view />

  </div>
</template>

<script>
import migrateCookieToLocalStorage from '@/utils/bian'
export default {
  name: 'App',
  created() {
    this.setCookie('test', 'hello', 1)
    migrateCookieToLocalStorage('test')
  },
  methods: {
    setCookie(name, value, hours) {
      const expires = new Date()
      expires.setHours(expires.getHours() + hours)
      const cookie = name + '=' + (value || '') + '; expires=' + expires.toUTCString()
      document.cookie = cookie
    }
  }
}
</script>

<style>

</style>
