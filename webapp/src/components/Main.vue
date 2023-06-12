<template>
  <NavbarView />
  <div class="container py-5">
    <div class="py-5"><h3>{{ head }}</h3></div>
    <div class="py-1">
      <form @submit.prevent="getCandidates('search')" class="form form-check" role="form">
        <div class="row">
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="region">Region</label>
              <input autocomplete="on" class="form-control mb-2 mr-sm-2 mb-sm-0" id="region" maxlength="25" minlength="2" v-model="region" name="region" placeholder="поиск по региону" type="text">
            </div>
          </div>
          <div class="col-md-4">
            <div class="mb-3">
              <label class="visually-hidden" for="fullname">Fullname</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="fullname" maxlength="250" minlength="3" v-model="fullname" name="fullname" placeholder="поиск по ФИО" type="text">
            </div>
          </div>
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="birthday">Birthday</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="birthday" v-model="birthday" name="birthday" placeholder="по дате рождения" type="date">
            </div>
          </div>
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="status">Status</label>
              <select class="form-select mb-2 mr-sm-2 mb-sm-0" v-model="status" name="status">
                <option value="">По региону</option>
                <option value="Новый">Новый</option>
                <option value="Обновлен">Обновлен</option>
                <option value="Проверка">Проверка</option>
                <option value="Сохранено">Сохранено</option>
                <option value="Автомат">Автомат</option>
                <option value="Робот">Робот</option>
                <option value="Обработано">Обработано</option>
                <option value="ПФО">ПФО</option>
                <option value="Результат">Результат</option>
                <option value="Ошибка">Ошибка</option>
              </select>
            </div>
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary btn-md" type="submit">Найти</button>
          </div>
        </div>
      </form>
    </div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="10%">#</th>
            <th width="15%">Регион</th>
            <th>Фамилия Имя Отчество</th>
            <th width="15%">Дата рождения</th>
            <th width="15%">Статус</th>
            <th width="15%">Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="candidate in candidates" :key="candidate.id">
            <td>{{ candidate.id }}</td>
            <td>{{ candidate.region }}</td>
            <td><router-link :to="{ name: 'profile', params: {id: candidate.id} }">{{ candidate.fullname }}</router-link></td>
            <td>{{ this.convertDate(candidate.birthday) }}</td>
            <td>{{ candidate.status }}</td>
            <td>{{ this.convertDate(candidate.deadline) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="hasPagination">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="nextPage">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import NavbarView from './Navbar.vue';

export default {
  name: 'MainApp',

  components: {
    NavbarView
  },

  data() {
    return {
      head: "Новые кандидаты",
      domen: "http://localhost:5000/",
      path: '',
      region: '',
      fullname: '',
      birthday: '',
      status: '',
      candidates: [],
      currentPage: '',
      currentPath: '',
      hasPagination: false,
      hasPrev: false,
      hasNext: false
    };
  },
  
  methods: {
    async getCandidates(path, page=1) {
      this.currentPage = page;
      this.currentPath = path;
      switch (path) {     
        case 'search':
          this.head = "Результаты поиска";
          break;
        case 'officer':
          this.head = "Страница пользователя";
          break;
        case 'main':
          this.head = "Главная страница"
          break;
        default:
          this.head = "Новые кандидаты";
      }
      let response
      if (path !== 'search') {
        response = await fetch(`${this.domen}/index/${path}/${this.currentPage}`, {headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
          'Content-Type': 'application/json'
          }})
      } else {
        response = await fetch(`${this.domen}/index/${path}/${this.currentPage}`, {
          method: "POST",
          headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
          'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "region": this.region, 
            "fullname": this.fullname, 
            "birthday": this.birthday, 
            "status": this.status
          }),
        })
      }
      const [ data, metadata ] = await response.json();
      this.candidates = data;
      this.hasPagination = this.hasNext || this.hasPrev;
      this.hasPrev = metadata.has_prev;
      this.hasNext = metadata.has_next;
    },

    convertDate(value) {
      const date = new Date(Date.parse(value));
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const year = date.getFullYear().toString();
      return `${day}.${month}.${year}`;
    },

    async prevPage() {
      if (this.hasPrev) {
        this.currentPage -= 1;
        await this.getCandidates(this.currentPath, this.currentPage);
      }
    },

    async nextPage() {
      if (this.hasNext) {
        this.currentPage += 1;
        await this.getCandidates(this.currentPath, this.currentPage);
      }
    }
  },

  watch: {
    '$route.params.flag'(newVal) {
      this.path = newVal
      this.getCandidates(this.path)
    }
  },

  created() {
    this.path = this.$route.params.flag
    this.getCandidates(this.path)
  }
};
</script>
