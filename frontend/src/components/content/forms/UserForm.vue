<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { axiosAuth } from "@/auth";
import { stateAlert, stateClassify } from "@/state";
import { server, clearForm } from "@/utilities";
import { User } from "@/interfaces";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
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
    const response =
      props.action === "edit"
        ? await axiosAuth.patch(
            `${server}/user/${props.item["id"]}`,
            userForm.value
          )
        : await axiosAuth.post(`${server}/user`, userForm.value);
    console.log(response.status);
    if (props.action === "edit") {
      stateAlert.setAlert("alert-success", "Пользователь успешно изменен");
    } else {
      stateAlert.setAlert("alert-success", "Пользователь успешно создан");
    }
  } catch (error) {
    console.error(error);
    stateAlert.setAlert("alert-danger", "Ошибка сохранения данных");
  }
  clearForm(userForm.value);
  emit("update");
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
          :pattern="'[a-zA-Zа-яА-Я ]+'"
          v-model="userForm['fullname']"
        />
      </LabelSlot>
      <LabelSlot :label="'Учетная запись'">
        <InputElement
          :name="'username'"
          :place="'Учетная запись'"
          :pattern="'[a-zA-Z]+'"
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
        <SelectObject
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
          <BtnGroup :offset="false">
            <GroupContent
              :submit-btn="props.action === 'create' ? 'Создать' : 'Изменить'"
              @cancel="emit('cancel')"
            />
          </BtnGroup>
        </div>
      </div>
    </form>
  </div>
</template>
