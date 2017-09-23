<template>
  <div class="auth-debug">
    <h2>Auth API Debug</h2>

    <section>
      <div class="left">
        <img src="https://ru.facebookbrand.com/wp-content/uploads/2016/05/FB-fLogo-Blue-broadcast-2.png" width="75">
      </div>
      <div class="right">
        <h3><a :href="fbAuthUrl">Войти</a></h3>
        <p>Авторизация будет через: <br><code>{{fbAuthUrl}}</code></p>
        <p>Перенаправление будет на: <br><code>{{redirectUri('fb')}}</code></p>
        <!--<button href="" @click="connectFacebook()">Connect facebook</button>-->
        <p v-if="tokens.fb">Facebook токен: {{tokens.fb}}</p>
      </div>
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
      redirectUri (type) {
        return `${location.protocol}//${location.host}/fb-auth-success`
      }
    }

  }
</script>

<style>

  .auth-debug {
    margin: 60px;
    max-width: 45em;
  }

  .auth-debug h3:first-child,
  .auth-debug p:first-child {
    margin-top: 0px;
  }

  .auth-debug section {
    display: flex;
    margin: 50px auto;
  }

  .auth-debug section .left {
    padding-right: 3em;
  }

</style>
