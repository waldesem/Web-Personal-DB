<template>
  <NavbarView />
  <div class="container">
    <div class="py-5">
      <h5>{{title}}</h5>
    </div>
    <div class="py-1">
      <table class="table table-hover align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in candidates" :key="index">
            <td >{{value}}</td><td>{{name}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-2">
      <table class="table table-hover align-middle">
        <caption>Статистика по ПФО</caption>
        <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in poligraf" :key="index">
            <td >{{value}}</td><td>{{name}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-4">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-md-2" for="start">Начало периода</label>
              <div class="col-md-2">
                  <input class="form-control" name="start" required type="date" value="">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-md-2" for="end">Конец периода</label>
              <div class="col-md-2">
                  <input class="form-control" name="end" required type="date" value="">
              </div>
          </div>
          <div class=" row">
              <div class="offset-md-2 col-md-2">
                  <input class="btn btn-primary btn-md" name="submit" type="submit" value="Принять">
              </div>
          </div>
      </form>
    </div>
  </div>
</template>

<script>
import NavbarView from './Navbar.vue';

export default {
  name: 'StatApp',
  
  components: {
    NavbarView
  },

  data() {
    return {
      start: '',
      end: '',
      title: '',
      candidates: [],
      poligraf: [],
    };
  },

  methods: {
    async submitData(event) {
      const response = await fetch(`http://localhost:5000/information`, {
        method: 'POST',
        body: new FormData(event.target)
      });
      const { candidates, poligraf, title } = await response.json();
      this.candidates = candidates;
      this.poligraf = poligraf;
      this.title = title;
    }
  },

  async created () {
    const response = await fetch(`http://localhost:5000/information`);
    const { candidates, poligraf, title } = await response.json();
    this.candidates = candidates;
    this.poligraf = poligraf;
    this.title = title;
  }
};
</script>