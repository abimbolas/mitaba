import axios from 'axios'
import qs from 'qs'

class Api {
  constructor () {
    this.baseUrl = `${location.protocol}//${location.hostname}:8000`
    this.resource = axios.create({
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      },
      transformRequest: [function (data) {
        const transformed = qs.stringify({data: JSON.stringify(data)})
        return transformed
      }]
    })
  }

  get (path, data) {
    return this.resource
      .get(`${this.baseUrl}${path}?${qs.stringify(data)}`)
      .then(res => res.data)
  }

  post (path, data) {
    return this.resource
      .post(`${this.baseUrl}${path}`, data)
      .then(res => res.data)
  }
}

export default new Api()
