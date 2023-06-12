<template>
	<NavbarView />
	<div class="container py-3">
    <AlertMessage :attr="attr" :text="text" />
		<h5>{{ title }}</h5>
		<div class="py-3">
      <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
          <div class="col-lg-10">
            <input class="form-control" type="file" ref="fileInput">
          </div>
        </div>
      </form>
		</div>
		<BriefView />
	</div>
</template>

<script>
import NavbarView from './Navbar.vue';
import AlertMessage from './Message.vue';
import BriefView from './profile/BriefView.vue';

export default {
  name: 'LoginApp',

  components: {
    NavbarView,
    AlertMessage,
    BriefView
  },
  
  data() {
    return {
      attr: 'alert-info',
      text: 'Заполните поля или загрузите файл',
      title: 'Создать новую анкету',
      file: null
    };
  },

  methods: {
    
    async submitFile(event) {
      event.preventDefault();

      const formData = new FormData();
      formData.append('file', this.$refs.fileInput.files[0]);

      const response = await fetch(`http://localhost:5000/resume/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        },
      });
      const { message, cand_id } = await response.json();
      this.attr = "alert-success"
      this.text = message;
      this.$router.push({name: 'profile', params: {id: cand_id}})
    },
  }
}
</script>

