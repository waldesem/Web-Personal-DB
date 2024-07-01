<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { authErrorHandler, axiosAuth } from "@/auth";
import { stateAlert, stateClassify, server } from "@/state";
import { User } from "@/interfaces";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["update", "cancel"]);

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
    const response = await axiosAuth.post(
      `${server}/users`, userForm.value
    );
     if (response.status === 205) {
      stateAlert.setAlert("alert-warning", "Пользователь уже существует")
     } else {
      stateAlert.setAlert("alert-success", "Запись успешно добавлена");
    }
  } catch (error) {
    authErrorHandler(error);
  }
  emit("update");
  Object.keys(userForm.value).forEach(
    (key) => delete userForm.value[key as keyof typeof userForm.value]
  );
}
</script>

<template>
  <div class="p-3">
    <form @submit.prevent="submitUser" class="form form-check" role="form">
      <LabelSlot :label="'Имя пользователя'">
        <InputElement
          :name="'fullname'"
          :place="'Имя пользователя'"
          :need="props.action !== 'edit'"
          :pattern="'[А-Яа-я- ]+'"
          v-model="userForm['fullname']"
        />
      </LabelSlot>
      <LabelSlot :label="'Учетная запись'">
        <InputElement
          :name="'username'"
          :place="'Учетная запись'"
          :pattern="'[a-zA-Z_]+'"
          :need="props.action !== 'edit'"
          :disable="props.action === 'edit'"
          v-model="userForm['username']"
        />
      </LabelSlot>
      <LabelSlot :label="'Электронная почта'">
        <InputElement
          :name="'email'"
          :place="'Электронная почта'"
          :typeof="'email'"
          :need="props.action !== 'edit'"
          v-model="userForm['email']"
        />
      </LabelSlot>
      <LabelSlot :label="'Регион'">
        <SelectDiv
          :name="'region'"
          :place="'Регион'"
          :need="props.action !== 'edit'"
          :select="stateClassify.regions"
          v-model="userForm['region']"
        />
      </LabelSlot>
      <LabelSlot :label="'Администратор'">
        <SwitchBox :name="'admin'" v-model="userForm['has_admin']" />
      </LabelSlot>
      <div class="row m-3">
        <div class="col col-auto">
          <BtnGroup 
            :offset="false"
            :submit-btn="props.action === 'create' ? 'Создать' : 'Изменить'"
            @cancel="emit('cancel')"
          />
        </div>
      </div>
    </form>
  </div>
</template>
