<script setup lang="ts">
import { onBeforeMount, defineAsyncComponent, ref } from "vue";
import { stateUser, stateClassify, server } from "@/state";
import { axiosAuth } from "@/auth";
import { router } from "@/router";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/content/elements/ModalWin.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

onBeforeMount(async () => {
  await stateUser.getCurrentUser();
});

async function userLogout(): Promise<void> {
  localStorage.removeItem("user_token");
  router.push({ name: "login" });
}

const settings = ref({
  uri: "",
  path: "",
})

async function submitSettings(): Promise<void> {
  const setting = await axiosAuth.post(`${server}/settings`, settings.value);
  console.log(setting.status);
}
</script>

<template>
  <div class="container-fluid row ps-3">
    <div class="col-2 d-print-none">
      <div class="navbar navbar-expand sticky-top fs-5 p-3">
        <div class="nav flex-column">
          <a class="nav-link text-danger fs-3 fw-bold">STAFFSEC FINTECH</a>
          <hr class="text-info" />
          <router-link :to="{ name: 'persons' }" class="nav-link active">
            Кандидаты
          </router-link>
          <hr class="text-info" />
          <router-link :to="{ name: 'resume' }" class="nav-link active">
            Создать
          </router-link>
          <hr class="text-info" />
          <router-link :to="{ name: 'information' }" class="nav-link active">
            Информация
          </router-link>
          <hr class="text-info" />
          <router-link
            v-if="stateUser.user.role == stateClassify.classes.roles['admin']"
            :to="{ name: 'users' }"
            class="nav-link active"
          >
            Пользователи
          </router-link>
        </div>
      </div>
    </div>
    <div class="col-9" id="staffsec">
      <div class="sticky-top bg-white d-print-none p-3">
        <div class="row">
          <div class="col-10 text-center">
            <AlertMessage />
          </div>
          <div class="col-2 text-end">
            <div class="dropdown">
              <button
                class="btn btn-link btn-lg dropdown-toggle"
                style="text-decoration: none"
                role="button"
                data-bs-toggle="dropdown"
              >
              <i class="bi bi-person-circle"></i>
              {{ stateUser.user.username }}
              </button>
              <ul class="dropdown-menu">
                <li
                  v-if="stateUser.user.role == stateClassify.classes.roles['admin']" 
                  class="dropdown-item">
                  <a 
                    class="link-opacity-50-hover" 
                    href="#" 
                    data-bs-toggle="modal"
                    data-bs-target="#settings-modal"
                  >
                    Настроики
                  </a>
                </li>
                <li class="dropdown-item">
                  <a
                    class="link-opacity-50-hover"
                    href="#"
                    @click="userLogout"
                  >
                    Выход
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <router-view v-slot="{ Component }" :key="$route.fullPath">
        <component :is="Component" />
      </router-view>
    </div>
    <div class="col-1 d-print-none"></div>
  </div>
  <footer
    id="footer"
    class="d-flex justify-content-center border-top bg-white d-print-none"
  >
    <p class="text-muted mt-2">© 2024 STAFFSEC FINTECH</p>
  </footer>
  <ModalWin :elem-id="'settings-modal'">
    <form @submit.prevent="submitSettings" class="form form-check p-3" role="form">
      <LabelSlot 
        :label="'Папка базы данных'"
      >
        <InputElement
          :name="'path'"
          :need="true"
          :place="'Папка базы данных'"
          v-model="settings['path']"
        />
      </LabelSlot>
      <LabelSlot 
        :label="'URI базы данных'"
      >
        <InputElement
          :name="'uri'"
          :need="true"
          :place="'URI базы данных'"
          v-model="settings['uri']"
        />
      </LabelSlot>
      <BtnGroup />
    </form>
  </ModalWin>
</template>

<style scoped>
@media print {
  #staffsec {
    width: 100% !important;
  }
}
#staffsec {
  padding-bottom: 5vh;
}
footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 5vh;
}
</style>
