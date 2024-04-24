<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { axiosAuth } from "@/auth";
import { stateAlert } from "@/state";
import { server, clearForm } from "@/utilities";
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

const connectForm = toRef(props.item as Connection);

async function updateContact(): Promise<void> {
  try {
    const response =
      props.action === "create"
        ? await axiosAuth.post(
            `${server}/connect`,
            connectForm.value
          )
        : await axiosAuth.patch(
            `${server}/connect/${props.item["id"]}`,
            connectForm.value
          );
    console.log(response.status);

    const alert = {
      create: ["alert-success", "Контакт добавлен"],
      edit: ["alert-info", "Контакт обновлен"],
    };
    stateAlert.setAlert(
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
}
</script>

<template>
  <form 
    @submit.prevent="updateContact; clearForm(connectForm)" 
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид контакта'">
      <InputElement
        :place="'Вид'"
        :name="'name'"
        :lst="'names'"
        :selects="props.names"
        v-model="connectForm['name']"
      />
    </LabelSlot>
    <LabelSlot :label="'Компания'">
      <InputElement
        :place="'Название'"
        :name="'company'"
        :lst="'companies'"
        :selects="props.companies"
        v-model="connectForm['company']"
      />
    </LabelSlot>
    <LabelSlot :label="'Город'">
      <InputElement
        :name="'city'"
        :place="'Город'"
        :lst="'cities'"
        :selects="props.cities"
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
        v-model="connectForm['mail']"
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
      <GroupContent @cancel="emit('cancel-edit')" />
    </BtnGroup>
  </form>
</template>
