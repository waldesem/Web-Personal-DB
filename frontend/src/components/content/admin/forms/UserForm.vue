<script setup lang="ts">
import { ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const storeAlert = alertStore();
const storeAuth = authStore();

const props = defineProps({
  action: String,
  item: {
    type: Object as () => Record<string, any>,
    default: {},
  },
});

const emit = defineEmits(["update"]);

const userForm = ref({
  form: <Record<string, any>>{},

  submitUser: async function (): Promise<void> {
    try {
      const response =
        props.action === "edit"
          ? await storeAuth.axiosInstance.patch(
              `${server}/user/${props.item['id' ]}`,
              this.form
            )
          : await storeAuth.axiosInstance.post(`${server}/user`, this.form);

      const { message } = response.data;
      if (message === "Changed") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь успешно изменен"
        );
      } else {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь успешно создан"
        );
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        "Ошибка сохранения данных"
      );
    }
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("update");
  },
});
</script>

<template>
  <form
    @submit.prevent="userForm.submitUser"
    class="form form-check"
    role="form"
  >
    <div class="mb-3 row">
      <label 
        class="col-form-label col-lg-2" 
        for="fullname"
      >
        Имя пользователя: 
      </label>
      <div class="col-lg-10">
        <input 
          class="form-control"
          id="fullname"
          name="fullname"
          placeholder="Имя пользователя"
          pattern="[a-zA-Zа-яА-Я ]+"
          v-model="userForm.form['fullname']"
        />
      </div>
    </div>
    <div class="mb-3 row">
      <label
        class="col-form-label col-lg-2"
        for="username"
      >
        Учетная запись:
      </label>
      <div class="col-lg-10">
        <input
          class="form-control"
          id="username"
          name="username"
          placeholder="Логин"
          pattern="[a-zA-Z]+"
          v-model="userForm.form['username']"
          required
          :disabled="props.action === 'edit'"
        />
      </div>
    </div>
    <div class="mb-3 row">
      <label
        class="col-form-label col-lg-2"
        for="email"
      >
        Электронная почта:
      </label>
      <div class="col-lg-10">
        <input
          class="form-control"
          id="email"
          name="email"
          placeholder="Электронная почта"
          v-model="userForm.form['email']"
          required
          />
      </div>
    </div>

    <div class="row mb-3">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group" role="group">
          <button
            class="btn btn-outline-secondary"
            name="submit"
            type="submit"
            data-bs-dismiss="modal"
          >
            {{ props.action === "create" ? "Создать" : "Изменить" }}
          </button>
          <button 
            class="btn btn-outline-secondary" 
            name="reset" 
            type="reset">
            Очистить
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
