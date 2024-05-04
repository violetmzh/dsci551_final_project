<template>
  <div class="app-container">
    <el-card class="box-card">

      <el-divider></el-divider>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column fixed align="center" prop="code" label="Data encoding">
        </el-table-column>
        <el-table-column prop="hash" align="center" label="hash value">
        </el-table-column>
      </el-table>
    </el-card>

  </div>
</template>

<script>
import { getInfo } from '@/api/hash'
import { Message } from 'element-ui'

export default {
  data () {
    return {
      tableData: [],
      centerDialogVisible: false,
      dialog: 0,
      roles: null,
      from: {
        code: null,
        hash: null
      }
    }
  },
  created () {
    this.getList()

  },
  methods: {
    getList () {
      this.roles = localStorage.getItem("role")
      getInfo().then(res => {
        this.tableData = res.data
      })
    },
    handleClick (row, type) {
      this.centerDialogVisible = !this.centerDialogVisible
      this.dialog = type
      if (row == null) {
        this.from = {
          code: null,
          hash: null
        }
      } else {
        this.from = row
      }
    },
    fromSubmit () {
      if (this.dialog === 0) {
        addCity(this.from).then(res => {
          Message({
            message: 'successfully added',
            type: 'success',
            duration: 2 * 1000
          })
          this.getList()
          this.centerDialogVisible = !this.centerDialogVisible
        })
      } else {
        editCity(this.from).then(res => {
          Message({
            message: 'Modified successfully',
            type: 'success',
            duration: 2 * 1000
          })
          this.getList()
          this.centerDialogVisible = !this.centerDialogVisible
        })
      }
    },
    removeSubmit (obj) {
      removeCity(obj).then(res => {
        Message({
          message: 'Successfully deleted',
          type: 'success',
          duration: 2 * 1000
        })
        this.getList()
      })
    }
  }
}
</script>
