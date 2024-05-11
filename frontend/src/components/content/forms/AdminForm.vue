<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, ref } from "vue";
import { stateAlert } from "@/state";
import { server, clearForm } from "@/utilities";
import { User } from "@/interfaces";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
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
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const emit = defineEmits(["update"]);

const userForm = ref(<User>{});

async function submitAdmin(): Promise<void> {
  try {
    const response = await axios.post(`${server}/users/admin`, userForm.value);
    if (response.status === 200) {
      stateAlert.setAlert(
        "alert-success",
        "Администратор успешно создан"
      )
      router.push({ name: "persons" });
    } else {
      stateAlert.setAlert(
        "alert-danger",
        "Администратор уже существует или некорректно введены данные"
      )
      router.push({ name: "admin" });
    }
  } catch (error) {
    console.error(error);
  }
  clearForm(userForm.value);
  emit("update");
}
</script>

<template>
  <div class="border border-primary rounded p-5">
    <HeaderDiv 
      :cls="'text-primary mb-3 text-center'"
      :page-header="'Создать администратора'" 
    />
    <form
      @submit.prevent="submitAdmin"
      class="form form-check border rounded p-"
      role="form"
    >
      <div class="mb-3">
        <LabelSlot :label="'Имя пользователя'">
          <InputElement
            :name="'fullname'"
            :place="'Имя пользователя'"
            :pattern="'[a-zA-Zа-яА-Я ]+'"
            v-model="userForm['fullname']"
          />
        </LabelSlot>
        <LabelSlot :label="'Логин'">
          <InputElement
            :name="'username'"
            :place="'Учетная запись'"
            :pattern="'[a-zA-Z]+'"
            v-model="userForm['username']"
          />
        </LabelSlot>
        <LabelSlot :label="'Электронная почта'">
          <InputElement
            :name="'email'"
            :place="'Электронная почта'"
            :typeof="'email'"
            v-model="userForm['email']"
          />
        </LabelSlot>
          <BtnGroup :offset="false">
            <GroupContent
              :submit-btn="'Создать'"
            />
          </BtnGroup>
      </div>
    </form>
  </div>
</template>
