<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { stateAlert, stateAnketa, stateClassify } from "@/state";
import { Persons } from "@/interfaces";
import { server } from "@/utilities";
import { router } from "@/router";
import { axiosAuth } from "@/auth";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  action: {
    type: String,
    default: "create",
  },
  resume: {
    type: Object as () => Persons,
    default: {},
  },
});

const resumeForm = toRef(props.resume);

async function submitResume(): Promise<void> {
  try {
    const response = await axiosAuth.post(`${server}/persons`, resumeForm.value);
    const { person_id } = response.data;

    Object.keys(resumeForm.value).forEach(
      (key) => delete resumeForm.value[key as keyof typeof resumeForm.value]
    );
    if (props.action === "create") {
      router.push({ name: "profile", params: { id: person_id } });
    } else {
      emit("cancel");
      stateAnketa.getItem("persons");
    }

    stateAlert.setAlert("alert-success", "Данные успешно обновлены");
  } catch (error) {
    stateAlert.setAlert("alert-danger", `Возникла ошибка ${error}`);
  }
}
</script>

<template>
  <form @submit.prevent="submitResume" class="form form-check" role="form">
    <LabelSlot :label="'Регион'">
      <SelectDiv
        :name="'region_id'"
        :select="stateClassify.regions"
        v-model="resumeForm['region']"
      />
    </LabelSlot>
    <LabelSlot :label="'Фамилия'">
      <InputElement
        :need="true"
        :name="'surname'"
        :place="'Фамилия*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm['surname']"
      />
    </LabelSlot>
    <LabelSlot :label="'Имя'">
      <InputElement
        :need="true"
        :name="'firstname'"
        :place="'Имя*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm['firstname']"
      />
    </LabelSlot>
    <LabelSlot :label="'Отчество'">
      <InputElement
        :name="'patronymic'"
        :place="'Отчество'"
        v-model="resumeForm['patronymic']"
      />
    </LabelSlot>
    <LabelSlot :label="'Дата рождения*'">
      <InputElement
        :need="true"
        :name="'birthday'"
        :place="'Дата рождения*'"
        :typeof="'date'"
        v-model="resumeForm['birthday']"
      />
    </LabelSlot>
    <LabelSlot :label="'Место рождения'">
      <InputElement
        :name="'birthplace'"
        :place="'Место рождения'"
        v-model="resumeForm['birthplace']"
      />
    </LabelSlot>
    <LabelSlot :label="'Гражданство'">
      <InputElement
        :name="'citizenship'"
        :place="'Гражданство'"
        v-model="resumeForm['citizenship']"
      />
    </LabelSlot>
    <LabelSlot :label="'Двойное гражданство'">
      <InputElement
        :name="'dual'"
        :place="'Двойное гражданство'"
        v-model="resumeForm['dual']"
      />
    </LabelSlot>
    <LabelSlot :label="'СНИЛС'">
      <InputElement
        :name="'snils'"
        :place="'СНИЛС'"
        :pattern="'[0-9]{11}'"
        v-model="resumeForm['snils']"
      />
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      <InputElement
        :name="'inn'"
        :place="'ИНН'"
        :max="'12'"
        :pattern="'[0-9]{12}'"
        v-model="resumeForm['inn']"
      />
    </LabelSlot>
    <LabelSlot :label="'Семейное положение'">
      <InputElement
        :name="'marital'"
        :place="'Семейное положение'"
        v-model="resumeForm['marital']"
      />
    </LabelSlot>
    <LabelSlot :label="'Дополнительно'">
      <TextArea
        :name="'addition'"
        :place="'Дополнительно'"
        v-model="resumeForm['addition']"
      ></TextArea>
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')" />
  </form>
</template>
