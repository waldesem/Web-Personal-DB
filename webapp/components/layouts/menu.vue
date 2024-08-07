<script setup lang="ts">
import { stateUser, stateClassify } from "@/state/state";

const classify = stateClassify();
const userState = stateUser();

async function removeToken(): Promise<void> {
  localStorage.removeItem("user_token");
}
</script>

<template>
  <div class="container-fluid row ps-3">
    <div class="col-2 d-print-none">
      <div class="navbar navbar-expand sticky-top fs-5 p-3">
        <div class="nav flex-column">
          <a class="nav-link text-danger fs-3 fw-bold">STAFFSEC FINTECH</a>
          <hr class="text-info" />
          <NuxtLink to="/persons" class="nav-link active">
            Кандидаты
          </NuxtLink>
          <hr class="text-info" />
          <NuxtLink
            v-if="userState.user.value.role == classify.classes.value.roles['user']"
            to="/resume"
            class="nav-link active"
          >
            Создать
          </NuxtLink>
          <hr
            v-if="userState.user.value.role == classify.classes.value.roles['user']"
            class="text-info"
          />
          <NuxtLink to="/info" class="nav-link active">
            Информация
          </NuxtLink>
          <hr class="text-info" />
          <NuxtLink
            v-if="userState.user.value.role == classify.classes.value.roles['admin']"
            to="/users"
            class="nav-link active"
          >
            Пользователи
          </NuxtLink>
        </div>
      </div>
    </div>
    <div class="col-9" id="staffsec">
      <div class="sticky-top bg-white d-print-none p-3">
        <div class="row">
          <div class="col-10 text-center">
            <DivsAlertMessage />
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
                {{ userState.user.value.username }}
              </button>
              <ul class="dropdown-menu">
                <li class="dropdown-item">
                  <NuxtLink
                    to="/login"
                    class="link-opacity-50-hover"
                    @click="removeToken"
                  >
                    Выход
                  </NuxtLink>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <slot></slot>
    </div>
    <div class="col-1 d-print-none"></div>
  </div>
  <footer
    id="footer"
    class="d-flex justify-content-center border-top bg-white d-print-none"
  >
    <p class="text-muted mt-2">© 2024 STAFFSEC FINTECH</p>
  </footer>
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
