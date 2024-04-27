<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { stateAlert, stateAnketa, stateClassify } from "@/state";
import { Resume } from "@/interfaces";
import { server, clearForm } from "@/utilities";
import { router } from "@/router";
import { axiosAuth } from "@/auth";


const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
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
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  action: {
    type: String,
    default: "create",
  },
  resume: {
    type: Object as () => Resume,
    default: {},
  }
});

const resumeForm = toRef(props.resume);

async function submitResume(): Promise<void> {
  try {
    const response =
      props.action === "create"
        ? await axiosAuth.post(
            `${server}/resume/${props.action}`,
            resumeForm.value
          )
        : await axiosAuth.patch(
            `${server}/resume/${stateAnketa.share.candId}`,
            resumeForm.value
          );
    const { message } = response.data;

    clearForm(resumeForm.value);
    
    if (props.action === "create") {
      router.push({ name: "profile", params: { id: message } })
    } else {
      emit("cancel");
       stateAnketa.getResume();
    };

    stateAlert.setAlert(
      "alert-success",
      "Данные успешно обновлены"
    );
  } catch (error) {
    stateAlert.setAlert(
      "alert-danger",
      `Возникла ошибка ${error}`
    );
  }
};
</script>

<template>
  <form
    @submit.prevent="submitResume"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Регион'">
      <SelectObject
        :name="'region_id'"
        :select="stateClassify.regions"
        v-model="resumeForm['region_id']"
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
        :name="'country'"
        :place="'Гражданство'"
        v-model="resumeForm['country']"
      />
    </LabelSlot>
    <LabelSlot :label="'Двойное гражданство'">
      <InputElement
        :name="'ext_country'"
        :place="'Двойное гражданство'"
        v-model="resumeForm['ext_country']"
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
    <LabelSlot :label="'Образование'">
      <TextArea
        :name="'education'"
        :place="'Образование'"
        v-model="resumeForm['education']"
      ></TextArea>
    </LabelSlot>
    <LabelSlot :label="'Дополнительно'">
      <TextArea
        :name="'addition'"
        :place="'Дополнительно'"
        v-model="resumeForm['addition']"
      ></TextArea>
    </LabelSlot>
    <BtnGroup>
      <GroupContent @cancel="emit('cancel')"/>
    </BtnGroup>
  </form>
</template>
