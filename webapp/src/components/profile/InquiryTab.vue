<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form" id="inquiryFormId">
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="info">Информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="info" name="info" required=""></textarea>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
        <div class="col-lg-10">
          <input class="form-control" id="initiator" maxlength="250" name="initiator" required="" type="text" value="">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="source">Источник</label>
        <div class="col-lg-10">
          <input class="form-control" id="source" maxlength="250" name="source" required="" type="text" value="">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата запроса</label>
        <div class="col-lg-10">
          <input class="form-control" id="deadline" name="deadline" required="" type="date" value="2023-05-16">
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
    <a @click="url = 'inquiry'" class="btn btn-outline-primary" type="button">Добавить запись</a>
  </template>
</template>

<script>

export default {
  name: 'InquiryView',
  
  props: {
    table: String,
    candId: String
  },
  
  emits: ['updateMessage', 'updateItem'],

  data() {
    return {
      url: ''
    }
  },

  methods: {

    async submitData(event) {
      const response = await fetch(`http://localhost:5000/${this.url}/${this.candId}`, {
        method: "POST", 
        body: new FormData(event.target),
				headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
      });
      const { message } = await response.json();
      this.$emit('updateMessage', {
        attr: "alert-primary",
        text: message
      });
      this.$emit('updateItem')
      this.url = ''
    }
  }
}

</script>
