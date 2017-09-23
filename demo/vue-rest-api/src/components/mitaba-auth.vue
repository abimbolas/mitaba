<template>
  <div class="auth-debug">
    <h2>Auth API Debug</h2>

    <section>
      <h3>Facebook</h3>
      <a :href="fbAuthUrl">Auth</a>
      <p>{{redirectUri('fb')}}</p>
      <!--<button href="" @click="connectFacebook()">Connect facebook</button>-->
      <p>Facebook token: {{tokens.fb}}</p>
    </section>

  </div>
</template>

<script>
  export default {
    data () {
      return {
        tokens: {
          fb: ''
        }
      }
    },
    computed: {
      fbAuthUrl () {
        const clientId = '498893767146355'
        const scope = 'email'
        return `https://www.facebook.com/v2.10/dialog/oauth?client_id=${clientId}&redirect_uri=${encodeURI(this.redirectUri('fb'))}&scope=${scope}&response_type=code`
      }
    },
    methods: {
      connectFacebook () {
        // open url wi
        this.tokens.fb = 'LOL'

//        this.tokens.fb = url
//        location.replace(url)
      },

      redirectUri (type) {
//        const paths = {
//          vk: `/#/vk-auth-success`,
//          fb: `/#/fb-auth-success`
//        }
//        return `${location.protocol}//${location.host}${paths[type]}`
        return `http://local.candyface:8080/success_cb`
      }
    }

  }
</script>

<style>

</style>
