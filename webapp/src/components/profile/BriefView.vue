<template>
  <div class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" v-model="region" name="region">
            <option value="ГО">ГО</option>
            <option value="Томск">Томск</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Юг">РЦ Юг</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Урал">РЦ Урал</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" v-model="fullname" name="fullname" required type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="previous" name="previous" type="text">
        </div>
        </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения</label>
        <div class="col-lg-10">
          <input class="form-control" v-model="birthday" name="birthday" required type="date">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="birthplace" name="birthplace" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" v-model="country" name="country" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" v-model="snils" name="snils" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" v-model="inn" name="inn" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="education" name="education" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" v-model="addition" name="addition"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="recruiter">Рекрутер</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="recruiter" name="recruiter" type="text">
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
</template>

<script>
export default {
  name: 'BriefView',
  
  props: {
    resume: Object
  },

  emits: ['updateMessage', 'updateItem'],

  data() {
    return {
      region: '',
      fullname: '',
      previous: '',
      birthday: '',
      birthplace: '',
      country: '',
      snils: '',
      inn: '',
      education: '',
      addition: '',
      recruiter: ''
    };
  },

  methods: {

    async submitData() {
      const response = await fetch(`http://localhost:5000/resume/create`, {
      method: 'POST',
      body: JSON.stringify({
        region: this.region,
        fullname: this.fullname,
        previous: this.previous,
        birthday: this.birthday,
        birthplace: this.birthplace,
        country: this.country,
        snils: this.snils,
        inn: this.inn,
        education: this.education,
        addition: this.addition,
        recruiter: this.recruiter
      }),
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        'Content-Type': 'application/json'
        }
      });
      const { message, cand_id } = await response.json();
      this.$emit('updateMessage', {
        attr: "alert-success",
        text: message
      });
      console.log(cand_id);
      this.$emit('updateItem')
    }
  },

  created () {
    if (this.resume) {
      this.title = 'Создать новую анкету';
      this.region = this.resume.region;
      this.fullname = this.resume.fullname;
      this.previous = this.resume.previous;
      this.birthday = this.resume.birthday;
      this.birthplace = this.resume.birthplace;
      this.country = this.resume.country;
      this.snils = this.resume.snils;
      this.inn = this.resume.inn;
      this.education = this.resume.education;
      this.addition = this.resume.addition;
      this.recruiter = this.resume.recruiter;
		}
	}
}
</script>

