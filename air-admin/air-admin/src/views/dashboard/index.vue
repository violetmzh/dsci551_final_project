<template>
  <div class="dashboard-container">
    <div class="dashboard"></div>
    <div class="dashboard-image">
      <img src="@/assets/images/welcome.jpg" alt="dashboard-image">
    </div>
  </div>
</template>

<script>
import {
  mapGetters
} from 'vuex'

export default {
  name: 'Dashboard',
  data () {
    return {
      username: localStorage.getItem('username')
    }
  },
  created () {

  },
  computed: {

  }
}
</script>

<style lang="scss" scoped>
</style>