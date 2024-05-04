import request from '@/utils/request'

export function getInfo(token) {
  return request({
    url: '/select-all-set',
    method: 'get'
  })
}

