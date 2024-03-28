<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/admin/elements/InputLabel.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const emit = defineEmits(["update"]);

const props = defineProps({
  action: {
    type: String,
    default: "",
  },
  item: {
    type: Object as () => User,
    default: {},
  },
});

const userForm = computed(() => {
  return props.item as Record<string, any>;
});

async function submitUser(): Promise<void> {
  try {
    const response =
      props.action === "edit"
        ? await storeAuth.axiosInstance.patch(
            `${server}/user/${props.item['id' ]}`,
            userForm.value
          )
        : await storeAuth.axiosInstance.post(
          `${server}/user`, userForm.value
          );

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
  emit("update");
};
</script>

<template>
  <div class="p-3">
    <form
      @submit.prevent="submitUser"
      class="form form-check border rounded p-"
      role="form"
    > 
      <div class="row m-3">
        <div class="col col-auto">
          <InputLabel
            :name="'fullname'"
            :label="'Имя пользователя'"
            :pattern="'[a-zA-Zа-яА-Я ]+'"
            v-model="userForm['fullname']"
          />
        </div>
        <div class="col col-auto">
          <InputLabel
            :name="'username'"
            :label="'Учетная запись'"
            :pattern="'[a-zA-Z]+'"
            :disabled="props.action === 'edit'"
            v-model="userForm['username']"
          />
        </div>
        <div class="col col-auto">
          <InputLabel
            :name="'email'"
            :label="'Электронная почта'"
            :typeof="'email'"
            v-model="userForm['email']"
          />
        </div>
        <div class="col col-auto">
          <div class="btn-group" role="group">
            <button
              class="btn btn-secondary"
              name="submit"
              type="submit"
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
  </div>
</template>
