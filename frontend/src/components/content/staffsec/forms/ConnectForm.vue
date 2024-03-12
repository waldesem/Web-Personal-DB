<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { server } from "@utilities/utils";
import { Connection, ConnectionForm } from "@/interfaces/interface";

const InputSmall = defineAsyncComponent(
  () => import("@components/elements/InputSmall.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

const props = defineProps({
  page: Number,
  action: String,
  names: {
    type: Array<string>,
    default: [],
  },
  companies: {
    type: Array<string>,
    default: [],
  },
  cities: {
    type: Array<string>,
    default: [],
  },
  item: {
    type: Object as () => Connection,
    default: {},
  },
});

const connectForm = toRef(props.item as ConnectionForm);

async function updateContact(): Promise<void> {
  try {
    const response =
      props.action === "create"
        ? await storeAuth.axiosInstance.post(
          `${server}/connect`, 
          connectForm.value
          )
        : await storeAuth.axiosInstance.patch(
            `${server}/connect/${props.item['id']}`,
            connectForm.value
          );
    console.log(response.status);

    const alert = {
      create: ["alert-success", "Контакт добавлен"],
      edit: ["alert-info", "Контакт обновлен"],
    };
    storeAlert.alertMessage.setAlert(
      alert[props.action as keyof typeof alert][0],
      alert[props.action as keyof typeof alert][1]
    );
    Object.keys(connectForm.value).forEach((key) => {
      delete connectForm.value[key as keyof typeof connectForm.value];
    });
  } catch (error) {
    console.log(error);
  }
};
</script>

<template>
  <form @submit.prevent="updateContact" class="form form-check">
    <InputSmall
      :need="true"
      :title="'name'"
      :place="'Вид'"
      :lst="'names'"
      :selects="props.names"
      v-model="item['name']"
    />
    <InputSmall
      :need="true"
      :title="'company'"
      :place="'Название'"
      :lst="'companies'"
      :selects="props.companies"
      v-model="item['company']"
    />
    <InputSmall
      :title="'city'"
      :place="'Город'"
      :lst="'cities'"
      :selects="props.cities"
      v-model="connectForm['city']"
    />
    <InputSmall
      :title="'fullname'"
      :place="'Имя'"
      v-model="connectForm['fullname']"
    />
    <InputSmall
      :title="'phone'"
      :place="'Телефон'"
      v-model="connectForm['phone']"
    />
    <InputSmall
      :title="'adding'"
      :place="'Добав'"
      v-model="connectForm['adding']"
    />
    <InputSmall
      :title="'mobile'"
      :place="'Мобильный'"
      v-model="connectForm['mobile']"
    />
    <InputSmall
      :title="'mail'"
      :place="'Почта'"
      v-model="connectForm['mail']"
    />
    <InputSmall
      :title="'comment'"
      :place="'Комментарий'"
      v-model="connectForm['comment']"
    />
    <BtnGroup :cls="false">
      <button
        class="btn btn-outline-primary"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button
        class="btn btn-outline-secondary"
        name="reset"
        type="reset"
      >
        Очистить
      </button>
    </BtnGroup>
  </form>
</template>
