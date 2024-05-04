import request from '@/utils/request'

export function login(data) {
  return request({
    url: `/login`,
    method: 'post',
    data
  })
}

export function resign(data) {
  return request({
    url: `/resign`,
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/select-all-user',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}


export function addUser(data){
  return request({
    url:'/add-user',
    method: 'post',
    data
  })
}

export function editUser(data){
  return request({
    url:'/update-user',
    method: 'post',
    data
  })
}

export function removeUser(data){
  return request({
    url:'/remove-user',
    method: 'post',
    data
  })
}
