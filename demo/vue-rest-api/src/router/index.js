import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Auth from '@/components/mitaba-auth'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
      path: '/facebook-auth-redirect',
      name: 'facebook-auth-redirect',
      component: Auth
    },
    {
      path: '/vkontakte-auth-redirect',
      name: 'vkontakte-auth-redirect',
      component: Auth
    },
    {
      path: '/google-auth-redirect',
      name: 'google-auth-redirect',
      component: Auth
    }
  ]
})
