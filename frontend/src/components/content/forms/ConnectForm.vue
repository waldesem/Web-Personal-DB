<script setup lang="ts">
import  axios from "axios";
import { onBeforeMount, defineAsyncComponent, ref, toRef } from "vue";
import { axiosAuth } from "@/auth";
import { stateAlert } from "@/state";
import { server } from "@/utilities";
import { Connection } from "@/interfaces";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["get-contacts", "cancel-edit"]);

const props = defineProps({
  item: {
    type: Object as () => Connection,
    default: {},
  },
});

onBeforeMount(async () => {
  await getConnectors();
});

const connectorsData = ref({
  view: [],
  companies: [],
  cities: [],
});

async function getConnectors(): Promise<void> {
  try {
    const response = await axios.get(`${server}/connectors`);
    const { view, companies, cities } = response.data;
    Object.assign(connectorsData.value, {
      view: view,
      companies: companies,
      cities: cities,
    });
  } catch (error) {
    console.error(error);
  }
};

const connectForm = toRef(props.item as Connection);

async function updateContact(): Promise<void> {
  try {
    const response = await axiosAuth.post(
      `${server}/connects`, connectForm.value
    )
    console.log(response.status);
    stateAlert.setAlert("alert-success", "Измненения успешно записаны")
  } catch (error) {
    console.log(error);
  }
  emit("get-contacts");
}
</script>

<template>
  <form 
    @submit.prevent="updateContact" 
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид организации'">
      <InputElement
        :place="'Вид'"
        :name="'name'"
        :lst="'names'"
        :selects="connectorsData.view"
        v-model="connectForm['view']"
      />
    </LabelSlot>
    <LabelSlot :label="'Компания'">
      <InputElement
        :place="'Название'"
        :name="'company'"
        :lst="'companies'"
        :selects="connectorsData.companies"
        v-model="connectForm['company']"
      />
    </LabelSlot>
    <LabelSlot :label="'Город'">
      <InputElement
        :name="'city'"
        :place="'Город'"
        :lst="'cities'"
        :selects="connectorsData.cities"
        v-model="connectForm['city']"
      />
    </LabelSlot>
    <LabelSlot :label="'Имя'">
      <InputElement
        :name="'fullname'"
        :place="'Имя'"
        v-model="connectForm['fullname']"
      />
    </LabelSlot>
    <LabelSlot :label="'Телефон'">
      <InputElement
        :name="'phone'"
        :place="'Телефон'"
        v-model="connectForm['phone']"
      />
    </LabelSlot>
    <LabelSlot :label="'Добавочный'">
      <InputElement
        :name="'adding'"
        :place="'Добав'"
        v-model="connectForm['adding']"
      />
    </LabelSlot>
    <LabelSlot :label="'Мобильный'">
      <InputElement
        :name="'mobile'"
        :place="'Мобильный'"
        v-model="connectForm['mobile']"
      />
    </LabelSlot>
    <LabelSlot :label="'E-mail'">
      <InputElement
        :name="'mail'"
        :place="'Почта'"
        v-model="connectForm['email']"
      />
    </LabelSlot>
    <LabelSlot :label="'Комментарий'">
      <InputElement
        :name="'comment'"
        :place="'Комментарий'"
        v-model="connectForm['comment']"
      />
    </LabelSlot>
    <BtnGroup>
      <GroupContent @cancel="emit('cancel-edit')"/>
    </BtnGroup>
  </form>
</template>
