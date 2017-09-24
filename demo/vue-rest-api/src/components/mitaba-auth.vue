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
        <p v-if="search.code">Facebook code: <br><code>{{search.code}}</code></p>
        <p v-if="search.token">Facebook token: <br><code>{{search.token}}</code></p>
      </div>
    </section>
    <section v-if="tokens.mitaba">
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
    </section>
  </div>
</template>

<script>
  const processFetchResponse = response => {
    if (response.status < 400) {
      return response.json()
    } else {
      return Promise.reject(response.json())
    }
  }

  export default {
    data () {
      return {
        user: {},
        entries: [],
        tokens: {
          fb: '',
          mitaba: ''
        },
        search: {
          code: '',
          token: ''
        }
      }
    },
    created () {
      let query = location.search
      query = query.split('?')
      if (query.length > 1) {
        query = query[1].split('&')
        query.forEach(group => {
          let keyvalue = group.split('=')
          if (keyvalue[0] === 'code') {
            this.search.code = keyvalue[1]
          }
        })
      }
      let hash = location.hash
      hash = hash.split('#')
      if (hash.length > 1) {
        hash = hash[1].split('&')
        hash.forEach(group => {
          let keyvalue = group.split('=')
          if (keyvalue[0] === 'access_token') {
            this.search.token = keyvalue[1]
          }
        })
      }
      if (this.search.token) {
        const query = {
          client_id: 'r9LvASxvlwAazWn5PuMr37KtPmObu0dnIkPxeteQ',
          client_secret: 'Sv4Bzoke8d7PuELvmUJUT0OKaA9lNz6gcvSisPmRj1fJ6eefX1JWCBHKzctJSDaIFqdFVnTW8vc240Y7Whuyko9QRovZAmHicxkWqZl0wj2enw10VsQfjWQ4eLVWGCnN',
          grant_type: 'convert_token',
          backend: 'facebook',
          token: this.search.token
        }
        let queryString = []
        for (const key in query) {
          queryString.push(`${key}=${query[key]}`)
        }
        queryString = queryString.join('&')
        fetch(`http://localhost:8000/auth/convert-token?${queryString}`, {
          method: 'POST'
        })
          .then(processFetchResponse)
          .then(token => {
            this.tokens.mitaba = token.access_token
            return fetch(`http://${location.hostname}:8000/entries?access_token=${this.tokens.mitaba}`, {
              method: 'GET'
            })
          })
          .then(processFetchResponse)
          .then(entries => {
            this.entries = entries
            return fetch(`http://${location.hostname}:8000/users?access_token=${this.tokens.mitaba}`, {
              method: 'GET'
            })
          })
          .then(processFetchResponse)
          .then(users => {
            this.user = users[0]
          })
          .catch(console.error)
      }
    },
    computed: {
      fbAuthUrl () {
        const clientId = '498893767146355'
        const scope = 'email'
        return `https://www.facebook.com/v2.10/dialog/oauth?client_id=${clientId}&redirect_uri=${encodeURI(this.redirectUri('fb'))}&scope=${scope}&response_type=token`
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

  .tag {
    border: 1px solid lightgray;
    border-radius: 2px;
    padding: 2px;
    margin: 2px 4px;
  }

</style>
