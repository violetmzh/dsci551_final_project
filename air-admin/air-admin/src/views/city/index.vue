<template>
  <div class="app-container">
    <el-card class="box-card">

<el-form label-width="80px">
  <el-form-item label="City">
    <el-input v-model="searchValue"></el-input>
  </el-form-item>
</el-form>  

<el-button
        type="primary"
        @click="search()"
        >Search</el-button
      >
      <el-button
        type="info"
        @click="canal()"
        >Cancel</el-button
      >

      <el-button
        type="primary"
        @click="handleClick(null, 0)"
        v-if="roles == 'admin'"
        >Add</el-button
      >
      <el-divider></el-divider>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column fixed align="center" prop="id" label="ID">
        </el-table-column>
        <el-table-column prop="city" align="center" label="City">
        </el-table-column>
        <el-table-column align="center" prop="year" label="Year">
        </el-table-column>
        <el-table-column align="center" prop="value" label="Population">
        </el-table-column>
        <el-table-column align="center" prop="pmtwo" label="PM2.5">
        </el-table-column>
        <el-table-column align="center" prop="humidity" label="Humidity">
        </el-table-column>
        <el-table-column align="center" prop="temperature" label="Temperature">
        </el-table-column>
        <el-table-column align="center" label="Modify" v-if="roles == 'admin'">
          <template slot-scope="scope">
            <el-button
              @click="handleClick(scope.row, 1)"
              type="text"
              size="small"
              >edit</el-button
            >
            <el-button type="text" size="small" @click="removeSubmit(scope.row)"
              >delete</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      :title="dialog === 0 ? 'Add' : 'Modify'"
      :visible.sync="centerDialogVisible"
      width="50%"
    >
      <el-form :model="from" label-width="80px" :label-position="'right'">
        <el-form-item label="City" prop="city">
          <el-input v-model="from.city"></el-input>
        </el-form-item>
        <el-form-item label="Year" prop="year">
          <el-input v-model="from.year"></el-input>
        </el-form-item>
        <el-form-item label="Population" prop="value">
          <el-input v-model="from.value"></el-input>
        </el-form-item>
        <el-form-item label="PM2.5" prop="pmtwo">
          <el-input v-model="from.pmtwo"></el-input>
        </el-form-item>
        <el-form-item label="Humidity" prop="humidity">
          <el-input v-model="from.humidity"></el-input>
        </el-form-item>
        <el-form-item label="Temperature" prop="temperature">
          <el-input v-model="from.temperature"></el-input>
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
import { getInfo, addCity, editCity, removeCity,searchCity } from '@/api/city'
import { Message } from 'element-ui'

export default {
  data () {
    return {
      searchValue:null,
      tableData: [],
      centerDialogVisible: false,
      dialog: 0,
      roles: null,
      from: {
        id: null,
        city: null,
        year: null,
        value: null,
        pmtwo: null,
        humidity: null,
        temperature: null
      }
    }
  },
  created () {
    this.getList()

  },
  methods: {
    search(){
      if(this.searchValue==null){
        return;
      }
      searchCity({
        city:this.searchValue
      }).then(res=>{
          this.tableData = res.data
      })
    },
    canal(){
      this.getList()
      this.searchValue = null
    },
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
          id: null,
          city: null,
          year: null,
          value: null,
          pmtwo: null,
          humidity: null,
          temperature: null
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
