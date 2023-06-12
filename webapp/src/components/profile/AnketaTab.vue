<template>
  <ModalView :candId="candId" :path="url"/>
  <BriefView v-if="brief" :resume="resume" @updateMessage="updateMessage" @updateItem="updateItem"/>
  <template v-else>
    <div v-html="table" class="py-3"></div>
    <div class="btn-group" role="group">
      <button @click="brief = true" class="btn btn-outline-primary">Изменить анкету</button>
      <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
      <button @click="sendResume" class="btn btn-outline-primary">Отправить на проверку</button>
      <div class="btn-group">
        <button type="button" class="btn btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
          Добавить данные
        </button>
        <ul class="dropdown-menu">
          <li><a @click="url = 'staff'" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#modalWin" href="#">Добавить должность</a></li>
          <li><a @click="url = 'document'" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#modalWin" href="#">Добавить документ</a></li>
          <li><a @click="url = 'address'" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#modalWin" href="#">Добавить адрес</a></li>
          <li><a @click="url = 'contact'" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#modalWin" href="#">Добавить контакт</a></li>
          <li><a @click="url = 'workplace'" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#modalWin" href="#">Добавить работу</a></li>
        </ul>
      </div>
    </div>
  </template>
</template>

<script>
import ModalView from './ModalTab.vue';
import BriefView from './BriefView.vue';

export default {
  name: 'AnketaView',

  components: {
    ModalView,
    BriefView
  },
  
  props: {
    table: String,
    candId: String,
    resume: Object,
    state: Object,
    status: String
  },
  
  emits: ['updateMessage', 'updateItem'],

  data() {
    return {
      url: '',
      brief: false
    }
  },

  methods: {

    updateMessage(data) {
      this.$emit('updateMessage', data);
    },

    updateItem() {
      this.$emit('updateItem');
      this.brief = false
    },

    async updateStatus() {
      const response = await fetch(`http://localhost:5000/resume/status/${this.candId}`, {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
          'Content-Type': 'application/json'
          });
      const { message } = await response.json();
      this.$emit('updateMessage', {
        attr: "alert-info",
        text: message
      });
      window.scrollTo(0,0)
    },

    async sendResume() {
      const response = await fetch(`http://localhost:5000/resume/send/${this.candId}`, {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        'Content-Type': 'application/json'
        });
      const { message } = await response.json();
      this.$emit('updateMessage', {
        attr: "alert-info",
        text: message
      });
      window.scrollTo(0,0)
    }
  }
}
</script>
