import request from '@/utils/request'

export function getInfo(token) {
  return request({
    url: '/select-all-index',
    method: 'get'
  })
}

export function searchCity(data){
  return request({
    url:'/search-city-index',
    method: 'post',
    data
  })
}


export function addCity(data){
  return request({
    url:'/add-index',
    method: 'post',
    data
  })
}

export function editCity(data){
  return request({
    url:'/update-index',
    method: 'post',
    data
  })
}

export function removeCity(data){
  return request({
    url:'/remove-index',
    method: 'post',
    data
  })
}
