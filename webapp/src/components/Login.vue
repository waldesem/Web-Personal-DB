<template>
  <router-view></router-view>
  <div class="container px-5 py-5">
    <div class="border border-primary px-5 py-5">
      <AlertMessage :attr="attr" :text="text" />
      <h5>{{title}}</h5>
      <div class ="py-3">
        <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="username">Логин: </label>
              <div class="col-lg-4">
                <input autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" placeholder="Логин*" required type="text" value="" pattern="[0-9a-zA-Z]+">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="password">Пароль: </label>
                  <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" name="password" placeholder="Пароль*" required type="password" value="" pattern="[0-9a-zA-Z]+">
                    <div v-if="path =='/login'" class="py-1"><a @click="changePswd" href="#">Изменить пароль</a></div>
                  </div>
              </div>
          <div v-if="path === '/login'" class=" row">
              <div class="offset-lg-1 col-lg-4">
                  <div class="mb-3 form-check"><input class="form-check-input" name="remember" type="checkbox" value="y">
                    <label class="form-check-label" for="remember">Запомнить </label>
                  </div>
              </div>
          </div>
          <div v-else>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="new_pswd">Новый: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" 
                    name="new_pswd" placeholder="Новый пароль" required type="password" value="" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-1" for="conf_pswd">Повтор: </label>
                <div class="col-lg-4">
                    <input autocomplete="current-password" class="form-control" minlength="3" maxlength="25" 
                    name="conf_pswd" placeholder="Подтверждение пароля" required type="password" value="" pattern="[0-9a-zA-Z]+">
                </div>
            </div>
          </div>
          <div class=" row">
              <div class="offset-lg-1 col-lg-4">
                  <input class="btn btn-primary btn-md" name="submit" type="submit" v-bind:value="value">
              </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AlertMessage from './Message.vue';

export default {
  name: 'LoginView',

  components: {
    AlertMessage
  },

  data() {
    return {
      attr: 'alert-info',
      text: 'Авторизуйтесь для входа в систему',
      title: 'Вход в систему',
      path: '/login',
      value: 'Войти'
    };
  },

  methods: {
    changePswd() {
      this.path = '/password',
      this.attr = 'alert-info',
      this.text = 'Заполните обязательные поля',
      this.title = 'Изменение пароля'
      this.value = 'Изменить'
    },

    async submitData(event) {
      const response = await fetch(`http://localhost:5000/${this.path}`, {
        method: 'POST',
        body: new FormData(event.target)
      });
      const { user, access_token } = await response.json();
      switch (user){
        case "None":
          this.attr = 'alert-warning';
          this.text = 'Неверный логин или пароль';
          break
        case "Overdue":
          this.attr = 'alert-warning';
          this.text = 'Пароль просрочен. Измените пароль';
          break
        case "Denied":
          this.attr = 'alert-warning';
          this.text = 'Пользователь не авторизован';
          break
        case "Not_match":
          this.attr = 'alert-warning';
          this.text = 'Введенные пароли не совпадают';
          break
        case "Success":
          this.attr = 'alert-success';
          this.text = 'Пароль установлен. Войдите с новым паролем';
          this.path = '/login';
          this.title = 'Вход в систему';
          this.value = 'Войти';
          break
        case "Authorized":
          localStorage.setItem('jwt_token', access_token);
          this.$router.push({name: 'index', params: {flag: 'new'}});
          break
        default:
          console.error(user);
      }
    }
  },
  
  created() {
    fetch('http://localhost:5000/logout');
    const token = localStorage.getItem('jwt_token');
    if (token) localStorage.removeItem('jwt_token')
  },
};
</script>
