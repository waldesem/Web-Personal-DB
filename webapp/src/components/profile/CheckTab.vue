<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="workplace" v-model="workplace"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="employee" v-model="employee"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="document" v-model="document"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">Проверка ИНН</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="inn" v-model="inn"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="debt" v-model="debt"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bankruptcy" v-model="bankruptcy"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bki" v-model="bki"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="courts" v-model="courts"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="affiliation" v-model="affiliation"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="terrorist" v-model="terrorist"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="mvd" v-model="mvd"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="internet" v-model="internet"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cronos" v-model="cronos"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cros" v-model="cros"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="addition" v-model="addition"></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="mb-3 form-check"><input class="form-check-input" id="pfo" v-model="pfo" type="checkbox" value="y">
            <label class="form-check-label" for="pfo">Полиграф</label>
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
        <div class="col-lg-10">
          <select class="form-select" id="conclusion" v-model="conclusion">
            <option value="Без замечаний">Без замечаний</option>
            <option value="С комментарием">С комментарием</option>
            <option value="Негатив">Негатив</option>
            <option value="Отмена">Отмена</option>
            <option value="Сохранено">Сохранено</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
        <div class="col-lg-10">
          <input class="form-control" id="comments" maxlength="250" v-model="comments" type="text">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проверки</label>
        <div class="col-lg-10">
          <input class="form-control" id="deadline" v-model="deadline" required="" type="date">
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" @click="url = ''">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
  <template v-else>
    <div v-html="table" class="py-3"></div>
    <div class="btn-group" role="group">
      <a @click="deleteCheck" class="btn btn-outline-primary">Удалить проверку</a>
      <a @click="addCheck" class="btn btn-outline-primary" type="button">Добавить проверку</a>
      <a @click="editCheck" class="btn btn-outline-primary" type="button">Изменить проверку</a>
    </div>
  </template>
</template>

<script>

export default {
  name: 'CheckView',
  
  props: {
    table: String,
    item: Object,
    candId: String,
    state: Object,
    status: String
  },

  emits: ['updateMessage', 'updateItem'],
  
  data() {
    return {
      url: '',
      workplace: '',
      employee: '',
      document: '',
      inn: '',
      debt: '',
      bankruptcy: '',
      bki: '',
      courts: '',
      affiliation: '',
      terrorist: '',
      mvd: '',
      internet: '',
      cronos: '',
      cros: '',
      addition: '',
      pfo: '',
      conclusion: '',
      comments: '',
      deadline: ''
    }
  },

  methods: {
    
    async submitData(){
      const response = await fetch(`http://localhost:5000/check/${this.url}/${this.candId}`, {
        method: "post",
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          workplace: this.workplace,
          employee: this.employee,
          document: this.document,
          inn: this.inn,
          debt: this.debt,
          bankruptcy: this.bankruptcy,
          bki: this.bki,
          courts: this.courts,
          affiliation: this.affiliation,
          terrorist: this.terrorist,
          mvd: this.mvd,
          internet: this.internet,
          cronos: this.cronos,
          cros: this.cros,
          addition: this.addition,
          pfo: this.pfo,
          conclusion: this.conclusion,
          comments: this.comments,
          deadline: this.deadline
        })
      });
      const { message } = await response.json();
      this.$emit('updateMessage', {
        attr: "alert-warning",
        text: message
      });
      this.$emit('updateItem')
      this.url = ''
    },
    
    async deleteCheck() {
      if (confirm("Вы действительно хотите удалить проверку?")) {
        const response = await fetch(`http://localhost:5000/check/delete/${this.candId}`, {headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
        }});
        const { message } = await response.json();
        this.$emit('updateMessage', {
          attr: "alert-warning",
          text: message
        });
        this.$emit('updateItem')
      }
    },

    async addCheck() {
      this.url = 'new';
      const status = await fetch(`http://localhost:5000/check/status/${this.candId}`, {headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        'Content-Type': 'application/json'
      }});
      const { message } = await status.json();
      this.$emit('updateMessage', {
        attr: "alert-info",
        text: message
      });
    },

    async editCheck() {
      if (this.item){
        this.url = 'edit';
        this.workplace = this.item.workplace;
        this.employee = this.item.employee;
        this.document = this.item.document;
        this.inn = this.item.inn;
        this.debt = this.item.debt;
        this.bankruptcy = this.item.bankruptcy;
        this.bki = this.item.bki;
        this.courts = this.item.courts;
        this.affiliation = this.item.affiliation;
        this.terrorist = this.item.terrorist;
        this.mvd = this.item.mvd;
        this.internet = this.item.internet;
        this.cronos = this.item.cronos;
        this.cros = this.item.cros;
        this.addition = this.item.addition;
        this.pfo = this.item.pfo;
        this.conclusion = this.item.conclusion;
        this.comments = this.item.comments;
        this.deadline = this.item.deadline;
      }
    }
  }
}
</script>
