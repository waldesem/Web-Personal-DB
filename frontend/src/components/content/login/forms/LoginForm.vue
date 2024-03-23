<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, ref } from "vue";
import { alertStore } from "@store/alert";
import { authStore } from "@/store/auth";
import { server } from "@utilities/utils";
import { router } from "@/router/router";

const DivLabelInput = defineAsyncComponent(
  () => import("@components/content/login/elements/DivLabelInput.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const loginData = ref({
  action: "login",
  hidden: true,
  form: <Record<string, any>>{},

  submitLogin: async function (): Promise<void> {
    this.hidden = true;
    if (this.action === "password") {
      if (this.form["password"] === this.form["new_pswd"]) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Старый и новый пароли совпадают"
        );
        return;
      }
      if (this.form["conf_pswd"] !== this.form["new_pswd"]) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Новый пароль и подтверждение не совпадают"
        );
        return;
      }
      delete this.form["conf_pswd"];
    }
    try {
      const response =
        this.action === "password"
          ? await axios.patch(`${server}/login`, this.form)
          : await axios.post(`${server}/login`, this.form);
      const { message, access_token, refresh_token } = response.data;

      switch (message) {
        case "Changed":
          this.action = "login";
          storeAlert.alertMessage.attr = "alert-success";
          storeAlert.alertMessage.text = "Войдите с новым паролем";
          break
          
        case "Authenticated":
          storeAuth.accessToken = access_token;
          storeAuth.refreshToken = refresh_token;
          router.push({name: "auth"});
          break;

        case "Overdue":
          this.action = "password";
          storeAlert.alertMessage.setAlert(
            "alert-warning",
            "Пароль просрочен. Измените пароль"
          );
          break;

        case "Denied":
          this.action = "login";
          storeAlert.alertMessage.setAlert(
            "alert-danger",
            "Неверный логин или пароль"
          );
          break;
      }
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-warning", error as string);
    }
  },
})
</script>

<template>
  <div class="border border-primary rounded p-5">
    <h5>
      {{
        loginData.action === "login"
          ? "Вход в систему"
          : "Изменить пароль"
      }}
    </h5>
    <div class="py-3">
      <form
        @submit.prevent="loginData.submitLogin"
        class="form form-check"
        role="form"
      >
        <DivLabelInput
          :name="'username'"
          :label="'Логин'"
          :min="3"
          :max="16"
          :pattern="'[a-zA-Z]+'"
          v-model="loginData.form['username']"
        />
        <DivLabelInput
          :name="'password'"
          :label="'Пароль'"
          :min="8"
          :max="16"
          :pattern="'[0-9a-zA-Z]+'"
          :type="loginData.hidden ? 'password' : 'text'"
          v-model="loginData.form['password']
        "
        >
          <span class="input-group-text">
              <a
                role="button"
                @click="loginData.hidden = !loginData.hidden"
              >
                <i :class="loginData.hidden ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
              </a>
          </span>
        </DivLabelInput>
        <div class="row mb-3 col-lg-10 offset-lg-2"
          v-show="loginData.action === 'login'">
          <a
            class="link-primary"
            href="#"
            @click="loginData.action = 'password'"
          >
            Изменить пароль
          </a>
        </div>
        <div v-if="loginData.action === 'password'">
          <DivLabelInput 
            :name="'new_pswd'"
            :label="'Новый'"
            :min="8"
            :max="16"
            :pattern="'[0-9a-zA-Z]+'"
            :type="loginData.hidden ? 'password' : 'text'"
            v-model="loginData.form['new_pswd']"
          />
          <DivLabelInput
            :name="'conf_pswd'"
            :label="'Повтор'"
            :min="8"
            :max="16"
            :pattern="'[0-9a-zA-Z]+'"
            :type="loginData.hidden ? 'password' : 'text'"
            v-model="loginData.form['conf_pswd']"
          />
        </div>
        <div class="row mb-3">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button 
                class="btn btn-primary btn-md" 
                name="submit" 
                type="submit"
              >
                {{ loginData.action === "login" ? "Войти" : "Изменить" }}
              </button>
              <button
                class="btn btn-secondary btn-md"
                name="cancel"
                type="button"
                @click="loginData.action = 'login'"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
