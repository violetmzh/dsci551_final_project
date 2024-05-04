<template>
  <div :class="{ 'has-logo': showLogo }">
    <logo v-if="showLogo" :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        v-if="role == 'admin'"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        mode="vertical"
        :default-active="activeMenu"
        :collapse="isCollapse"
        background-color="#304156"
        text-color="#ffffff"
        :unique-opened="false"
        active-text-color="#409eff"
        :collapse-transition="false"
      >
        <el-menu-item
          :index="it.id + ''"
          v-for="(it, i) in menu"
          :key="i"
          @click="handleMenu(it)"
        >
          <span slot="title">
            <i :class="it.icon"></i>
            {{ it.title }}</span
          ></el-menu-item
        >
      </el-menu>

      <el-menu
        v-else
        :default-active="defaultPath"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        mode="vertical"
      >
        <el-menu-item
          :index="it.id + ''"
          v-for="(it, i) in menu2"
          :key="i"
          @click="handleMenu(it)"
        >
          <span slot="title">
            <i :class="it.icon"></i>
            {{ it.title }}</span
          >
        </el-menu-item>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Logo from './Logo'
// import SidebarItem from './SidebarItem'
import variables from '@/styles/variables.scss'

export default {
  components: { Logo },
  // computed: {
  //   ...mapGetters([
  //     'sidebar'
  //   ]),
  //   routes() {
  //     return this.$router.options.routes
  //   },
  // activeMenu() {
  //   const route = this.$route
  //   const { meta, path } = route
  //   // if set path, the sidebar will highlight the path you set
  //   if (meta.activeMenu) {
  //     return meta.activeMenu
  //   }
  //   return path
  // },
  //   showLogo() {
  //     return this.$store.state.settings.sidebarLogo
  //   },
  //   variables() {
  //     return variables
  //   },
  data () {
    return {
      menu: [
        {
          id: 1,
          title: 'Home page', path: '/dashboard',
          role: '',
          icon: 'el-icon-s-home'
        }, {
          id: 2,
          title: 'User Info', path: '/user/user',
          role: 'admin',
          icon: 'el-icon-s-custom'
        }, {
          id: 3,
          title: 'Data', path: '/city/city',
          role: '',
          icon: 'el-icon-s-data'

        },{
          id: 5,
          title: 'Data Display', path: '/echart/echart',
          role: '',
          icon: 'el-icon-pie-chart'

        },
      ],
      menu2: [
        {
          id: 1,
          title: 'Home page', path: '/dashboard',
          role: '',
          icon: 'el-icon-s-home'
        }, {
          id: 3,
          title: 'Data', path: '/city/city',
          role: '',
          icon: 'el-icon-s-data'

        },{
          id: 5,
          title: 'Data Display', path: '/echart/echart',
          role: '',
          icon: 'el-icon-pie-chart'

        },
      ],
      role: '',
      defaultPath: ''
    }
  },
  created () {
    this.defaultPath = localStorage.getItem('path') || 1

    this.role = localStorage.getItem('role')
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    routes () {
      return this.$router.options.routes
    },
    activeMenu () {
      const route = this.$route
      const { meta, path } = route
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    showLogo () {
      return this.$store.state.settings.sidebarLogo
    },
    variables () {
      return variables
    },
    isCollapse () {
      return !this.sidebar.opened
    }
  },

  methods: {

    handleMenu (it) {
      console.log(it)
      this.$router.push(it.path)

      localStorage.setItem('path', it.id)
    },

    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>


<style lang="less" scoped>
/depp/ .el-menu {
  background: #304156;
  color: #fff;
}

.el-menu-item {
  color: #fff;
}

.el-menu-item.is-active {
  color: #409eff !important;
}
/deep/ .el-menu-vertical-demo .el-menu {
  background: #304156 !important;
}

.el-menu-item:focus,
.el-menu-item:hover {
  background: #304156;
}
// /depp/ .el-menu-item:focus,
/depp/ .el-menu-item:hover {
  outline: 0;
  background-color: #304156;
}
</style>
