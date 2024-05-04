<template>
  <div class="app-container">
    <el-card class="box-card">

      <el-button type="primary" @click="handleClick(null,0)">Add</el-button>
      <el-divider></el-divider>

      <el-table
        :data="tableData"
        border
        style="width: 100%">
        <el-table-column
          fixed
          align="center"
          prop="id"
          label="ID">
        </el-table-column>
        <el-table-column
          prop="name"
          align="center"
          label="Name">
        </el-table-column>
        <el-table-column
          align="center"
          prop="account"
          label="Account">
        </el-table-column>
        <el-table-column
          align="center"
          prop="password"
          label="Password">
        </el-table-column>

        <el-table-column
          prop="role"
          align="center"
          label="Role">
          <template slot-scope="scope">
            <div v-if="scope.row.role === 1">
              <el-tag>Administrator</el-tag>
            </div>
            <div v-else>
              <el-tag type="info">User</el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column
          align="center"
          label="Modify"
        >
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row,1)" type="text" size="small">edit</el-button>
            <el-button type="text" size="small" @click="removeSubmit(scope.row)">delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      :title="dialog===0?'Add':'Modify'"
      :visible.sync="centerDialogVisible"
      width="50%"
    >
      <el-form :model="from" label-width="80px" :label-position="'right'">
        <el-form-item label="Name" prop="name">
          <el-input v-model="from.name"></el-input>
        </el-form-item>
        <el-form-item label="Account" prop="account">
          <el-input v-model="from.account"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="from.password"></el-input>
        </el-form-item>
        <el-form-item label="Role" prop="role">
          <el-radio-group v-model="from.role">
            <el-radio :label="1">Administrator</el-radio>
            <el-radio :label="2">User</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="centerDialogVisible = false">cancel</el-button>
    <el-button type="primary" @click="fromSubmit">submit</el-button>
      </span>
    </el-dialog>


  </div>
</template>

<script>
import {getInfo, addUser, editUser, removeUser} from '@/api/user'
import {Message} from 'element-ui'

export default {
  data() {
    return {
      tableData: [],
      centerDialogVisible: false,
      dialog: 0,
      from: {
        id: null,
        account: null,
        name: null,
        password: null
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      getInfo().then(res => {
        this.tableData = res.data
      })
    },
    handleClick(row, type) {
      this.centerDialogVisible = !this.centerDialogVisible
      this.dialog = type
      if (row == null) {
        this.from = {
          account: null,
          id: null,
          name: null,
          password: null
        }
      } else {
        this.from = row
      }
    },
    fromSubmit() {
      if (this.dialog === 0) {
        addUser(this.from).then(res => {
          Message({
            message: 'successfully added',
            type: 'success',
            duration: 2 * 1000
          })
          this.getList()
          this.centerDialogVisible = !this.centerDialogVisible
        })
      } else {
        editUser(this.from).then(res => {
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
    removeSubmit(obj) {
      removeUser(obj).then(res => {
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
