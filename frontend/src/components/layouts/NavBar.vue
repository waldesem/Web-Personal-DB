<script setup lang="ts">
const props = defineProps({
  arg: String,
  brand: {
    type: String,
    required: true
  },
  fullName: String,
  logOut: {
    type: Function,
    required: true
  }
})
</script>

<template>
  <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark d-print-none"
    :class="props.arg"
  >
    <div class="container">
      <a class="navbar-brand">{{ props.brand.toUpperCase() }}</a>
      <div
        class="navbar-nav mr-auto collapse navbar-collapse"
        id="navbarContent"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <slot name="navbar"></slot>
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
                @click="props.logOut"
                >Выход</a
              >
            </li>
          </ul>
        </li>
      </div>
    </div>
  </nav>
</template>