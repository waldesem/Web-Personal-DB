<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const MessageDiv = defineAsyncComponent(
  () => import("@components/layouts/MessageDiv.vue")
);

const props = defineProps({
  pageIdentity: String,
  fullName: String,
  userLogout: {
    type: Function,
    required: true,
  }
});
</script>

<template>
  <nav
    v-if="props.pageIdentity"
    class="navbar navbar-expand navbar-nav mr-auto navbar-dark d-print-none"
    :class="`${pageIdentity === 'admins' ? 'bg-secondary' : 'bg-primary'}`"
  >
    <div class="container">
      <a class="navbar-brand">{{
        pageIdentity ? pageIdentity.toUpperCase() : ""
      }}</a>
      <div
        class="navbar-nav mr-auto collapse navbar-collapse"
        id="navbarContent"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <template v-if="props.pageIdentity.toLowerCase() === 'admins'">
            <li class="nav-item">
              <router-link
                :to="{ name: 'users', params: { group: 'admins' } }"
                class="nav-link active"
                href="#"
              >
                Пользователи
              </router-link>
            </li>

            <li class="nav-item">
              <router-link
                :to="{ name: 'table', params: { group: 'admins' } }"
                class="nav-link active"
                href="#"
              >
                Таблицы
              </router-link>
            </li>
          </template>

          <template v-if="props.pageIdentity.toLowerCase() === 'staffsec'">
            <li class="nav-item">
              <router-link
                :to="{ name: 'persons', params: { group: 'staffsec' } }"
                class="nav-link active"
              >
                Кандидаты
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ name: 'resume', params: { group: 'staffsec' } }"
                class="nav-link active"
              >
                Создать
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ name: 'information', params: { group: 'staffsec' } }"
                class="nav-link active"
              >
                Информация
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ name: 'contacts', params: { group: 'staffsec' } }"
                class="nav-link active"
              >
                Контакты
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ name: 'manager', params: { group: 'staffsec' } }"
                class="nav-link active"
                href="#"
              >
                Файлы
              </router-link>
            </li>
            <MessageDiv />
          </template>
        </ul>

        <li class="nav-item dropdown d-flex">
          <a
            href="#"
            class="nav-link active dropdown-toggle"
            role="button"
            data-bs-toggle="dropdown"
            :title="
              props.fullName ? props.fullName : ''
            "
          >
            {{
              props.fullName
                ? props.fullName
                    .split(" ")
                    .map((item) => item.charAt(0))
                    .join("")
                : ""
            }}
            <i class="bi bi-person-circle"></i>
          </a>
          <ul class="dropdown-menu">
            <li>
              <a
                class="dropdown-item"
                href="#"
                @click="props.userLogout"
                >Выход</a
              >
            </li>
          </ul>
        </li>
      </div>
    </div>
  </nav>
</template>