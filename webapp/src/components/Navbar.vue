<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-primary">
      <div class="container">
        <router-link :to="{ name: 'index', params: {flag: 'main'} }" class="nav-link active">StaffSec</router-link>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'new'} }" class="nav-link active">Кандидаты
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{news}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'resume' }" class="nav-link active">Создать</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'index', params: {flag: 'officer'} }" class="nav-link active">Кабинет
                <span class="position-absolute translate-middle badge rounded-pill text-bg-success">{{checks}}</span></router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ name: 'information' }" class="nav-link active">Информация</router-link>
            </li>
          </ul>                                
        </div>                        
        <div class="d-flex px-2">
          <router-link :to="{name: 'login'}" class="nav-link active">Выход</router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavbarView',
  
  data() {
  return {
    news: '',
    checks: ''
    }
  },

  async created () {
    const response = await fetch('http://localhost:5000/count', {headers: {
      'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
      'Content-Type': 'application/json'
      }});
    const { news, checks } = await response.json();
    this.news = news;
    this.checks = checks
  }
}
</script>