<template>
  <div class="auth-debug">
    <h2>Auth API Debug
      </small>
    </h2>

    <h4 v-if="profile.username">
      Авторизованый пользователь: {{profile.email}}<br>
      Записей: {{entries.length}}
    </h4>

    <section>
      <div class="left">
        <img src="https://ru.facebookbrand.com/wp-content/uploads/2016/05/FB-fLogo-Blue-broadcast-2.png" width="75">
      </div>
      <div class="right">
        <h3><a :href="authUrl('facebook')">Войти</a></h3>
        <p>Авторизация будет через: <br><code>{{authUrl('facebook')}}</code></p>
        <p>Перенаправление будет на: <br><code>{{redirectUri('facebook')}}</code></p>
        <p v-if="token.facebook">Facebook токен: <br><code class="code">{{token.facebook}}</code></p>
        <p v-if="token.mitaba">Mitaba токен: <br><code class="code">{{token.mitaba}}</code></p>
      </div>
    </section>

<!--     <section v-if="tokens.mitaba">
      <div class="left">
        <h2>Mitaba</h2>
        <p>Token: <br><code>{{tokens.mitaba}}</code></p>
        <div v-if="user">
          <p>User:</p>
          <ol>
            <li v-for="(value, key) in user">{{key}} : {{value}}</li>
          </ol>
        </div>
        <div v-if="entries">
          <p>Items:</p>
          <ol>
            <li v-for="entry in entries">
              <p>Id: {{entry.id}}</p>
              <p>Start: {{entry.start}}</p>
              <p>Stop: {{entry.stop}}</p>
              <p>Tags: <span class="tag"
                             v-for="detail in entry.details">{{detail}}</span></p>
              <p>OwnerID: {{entry.owner}}</p>
            </li>
          </ol>
        </div>
      </div>
    </section> -->
  </div>
</template>

<script>
  import Api from '@/api'
  import qs from 'qs'

  export default {
    data () {
      return {
        token: {
          facebook: '',
          mitaba: ''
        },
        profile: {},
        entries: []
      }
    },
    created () {
      // if authenticated
      if (this.$route.name === 'auth') {
        if (localStorage['MitabaToken']) {
          this.refreshUserData()
        }
      }

      // if redirected
      if (this.$route.name.match(/-auth-redirect/)) {
        this.authMitaba().then(this.refreshUserData)
      }
    },

    computed: {},

    methods: {
      redirectUri (type) {
        return `${location.protocol}//${location.host}/${type}-auth-redirect`
      },

      authUrl (provider) {
        const urls = {
          facebook: `https://www.facebook.com/v2.10/dialog/oauth?client_id=498893767146355&redirect_uri=${encodeURI(this.redirectUri('facebook'))}&scope=email&response_type=token`
        }
        return urls[provider]
      },

      refreshUserData () {
        this.token.mitaba = localStorage['MitabaToken']
        Api
          .get('/users/', { access_token: this.token.mitaba })
          .then(res => {
            this.profile = res[0]
          })
        Api
          .get('/entries/', { access_token: this.token.mitaba })
          .then(res => {
            this.entries = res
          })
      },

      authMitaba () {
        const provider = this.$route.name.match(/(\w+)-auth-redirect/)[1]
        if (provider === 'facebook') {
          const token = this.$route.hash.split('#access_token=')[1].split('&')[0]
          this.token.facebook = token
          const params = {
            client_id: 'mitaba-app-dev',
            grant_type: 'convert_token',
            backend: 'facebook',
            token
          }
          return Api
            .post(`/auth/convert-token?${qs.stringify(params)}`)
            .then(res => {
              this.token.mitaba = res.access_token
              localStorage['MitabaToken'] = this.token.mitaba
              this.$router.push({ name: 'auth' })
            })
        }
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

  .auth-debug .red {
    color: crimson;
  }

  .tag {
    border: 1px solid lightgray;
    border-radius: 2px;
    padding: 2px;
    margin: 2px 4px;
  }

</style>
