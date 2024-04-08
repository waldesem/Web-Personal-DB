<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
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

const userForm = toRef(props.item as Record<string, any>);

async function submitUser(): Promise<void> {
  try {
    const response =
      props.action === "edit"
        ? await storeAuth.axiosInstance.patch(
            `${server}/user/${props.item["id"]}`,
            userForm.value
          )
        : await storeAuth.axiosInstance.post(`${server}/user`, userForm.value);

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
}
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
          <InputElement
            :name="'fullname'"
            :place="'Имя пользователя'"
            :pattern="'[a-zA-Zа-яА-Я ]+'"
            v-model="userForm['fullname']"
          />
        </div>
        <div class="col col-auto">
          <InputElement
            :name="'username'"
            :place="'Учетная запись'"
            :pattern="'[a-zA-Z]+'"
            :disabled="props.action === 'edit'"
            v-model="userForm['username']"
          />
        </div>
        <div class="col col-auto">
          <InputElement
            :name="'email'"
            :place="'Электронная почта'"
            :typeof="'email'"
            v-model="userForm['email']"
          />
        </div>
        <div class="col col-auto">
          <BtnGroup :offset="false">
            <GroupContent
              :submit-btn="props.action === 'create' ? 'Создать' : 'Изменить'"
            />
          </BtnGroup>
        </div>
      </div>
    </form>
  </div>
</template>
