<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, ref } from "vue";
import { onBeforeRouteLeave } from "vue-router";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import router from "@/router/router";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);

const storeAlert = alertStore();

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.keys(loginData.value.form).forEach((key) => {
    delete loginData.value.form[key as keyof typeof loginData.value.form];
  });
  next();
});

const loginData = ref({
  action: "login",
  hidden: true,
  form: <Record<string, any>>{},

  submitLogin: async function (): Promise<void> {
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
          delete this.form["new_pswd"];
          delete this.form["conf_pswd"];
          break
          
        case "Authenticated":
          localStorage.setItem("refresh_token", refresh_token);
          localStorage.setItem("access_token", access_token);
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
        <InputLabel
          :label="'Логин'"
          :name="'username'"
          :need="true"
          :max="'16'"
          :min="'3'"
          :clsInput="'col-lg-8'"
          :place="'Логин'"
          :pattern="'[a-zA-Z]+'"
          @input-event="
            loginData.form['username'] = $event.target.value
          "
        />
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="password">Пароль: </label>
          <div class="col-lg-8">
            <div class="input-group">
              <input
                autocomplete="current-password"
                class="form-control"
                required
                id="password"
                name="password"
                minlength="8"
                maxlength="16"
                placeholder="Пароль"
                pattern="[0-9a-zA-Z]+"
                :type="loginData.hidden ? 'password' : 'text'"
                v-model="loginData.form['password']"
              />
              <span class="input-group-text">
                <a
                  role="button"
                  @click="
                    loginData.hidden = !loginData.hidden
                  "
                >
                  <i
                    :class="
                      loginData.hidden
                        ? 'bi bi-eye'
                        : 'bi bi-eye-slash'
                    "
                  ></i>
                </a>
              </span>
            </div>
            <div v-show="loginData.action === 'login'" class="py-2">
              <a
                class="link-primary"
                href="#"
                @click="loginData.action = 'password'"
              >
                Изменить пароль
              </a>
            </div>
          </div>
        </div>
        <div v-if="loginData.action === 'password'">
          <InputLabel
            :label="'Новый'"
            :name="'new_pswd'"
            :need="true"
            :max="'16'"
            :min="'8'"
            :clsInput="'col-lg-6'"
            :place="'Новый пароль'"
            :pattern="'[0-9a-zA-Z]+'"
            :typeof="loginData.hidden ? 'password' : 'text'"
            @input-event="
              loginData.form['new_pswd'] = $event.target.value
            "
          />
          <InputLabel
            :label="'Повтор'"
            :name="'conf_pswd'"
            :need="true"
            :max="'16'"
            :min="'8'"
            :clsInput="'col-lg-6'"
            :place="'Повторите новый пароль'"
            :pattern="'[0-9a-zA-Z]+'"
            :typeof="loginData.hidden ? 'password' : 'text'"
            @input-event="
              loginData.form['conf_pswd'] = $event.target.value
            "
          />
        </div>
        <div class="offset-lg-2 col-lg-10">
          <button class="btn btn-primary btn-md" name="submit" type="submit">
            {{ loginData.action === "login" ? "Войти" : "Изменить" }}
          </button>
          &nbsp;
          <button
            v-show="loginData.action === 'password'"
            class="btn btn-secondary btn-md"
            type="button"
            @click="loginData.action = 'login'"
          >
            Отменить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
