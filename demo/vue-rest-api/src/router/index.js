import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Auth from '@/components/mitaba-auth'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/auth',
      name: 'auth',
      component: Auth
    },
    {
      path: '/fb-auth-success',
      name: 'auth-success',
      component: Auth
    }
  ]
})
