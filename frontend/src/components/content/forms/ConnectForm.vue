<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { server } from "@utilities/utils";
import { Connection } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/InputLabel.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/BtnGroupContent.vue")
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
    type: Array,
    default: [],
  },
  companies: {
    type: Array,
    default: [],
  },
  cities: {
    type: Array,
    default: [],
  },
  item: {
    type: Object as () => Connection,
    default: {},
  },
});

const emit = defineEmits(["get-contacts", "cancel-edit"]);

const connectForm = computed(() => {
  return props.item as Connection;
});

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
  emit("get-contacts", props.page);
};
</script>

<template>
  <form @submit.prevent="updateContact" class="form form-check">
    <div class="row mb-3">
      <InputLabel
        :label="'Вид'"
        :name="'name'"
        :lst="'names'"
        :selects="props.names"
        v-model="connectForm['name']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :label="'Название'"
        :name="'company'"
        :lst="'companies'"
        :selects="props.companies"
        v-model="connectForm['company']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'city'"
        :label="'Город'"
        :lst="'cities'"
        :selects="props.cities"
        v-model="connectForm['city']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'fullname'"
        :label="'Имя'"
        v-model="connectForm['fullname']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'phone'"
        :label="'Телефон'"
        v-model="connectForm['phone']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'adding'"
        :label="'Добав'"
        v-model="connectForm['adding']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'mobile'"
        :label="'Мобильный'"
        v-model="connectForm['mobile']"
      />
    </div>
    <div class="row mb-3">
      <InputLabel
        :name="'mail'"
        :label="'Почта'"
        v-model="connectForm['mail']"
      />
    </div>
    <div class="row mb-3">
    <InputLabel
      :name="'comment'"
      :label="'Комментарий'"
      v-model="connectForm['comment']"
    />
    </div>
    <BtnGroup>
      <BtnGroupContent/>
      <button
        class="btn btn-outline-secondary"
        name="cancel"
        type="button"
        @click="emit('cancel-edit')"
      >
        Отмена
      </button>
    </BtnGroup>
  </form>
</template>
