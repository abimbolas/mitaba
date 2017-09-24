import Vue from 'vue'
import Router from 'vue-router'
import Auth from '@/components/mitaba-auth'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
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
