<script setup lang="ts">
import { defineAsyncComponent, ref, computed } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
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

const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore();

const emit = defineEmits(["get-resume", "cancel", "submit"]);

const props = defineProps({
  action: {
    type: String,
    default: "create",
  },
  resume: {
    type: Object as () => Resume,
    default: {},
  },
});

const resumeForm = ref({
  form: computed(() => {
    return props.resume as Resume;
  }),

  submitResume: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/resume/${props.action}`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/resume/${props.resume["id"]}`,
              this.form
            );
      const { message } = response.data;

      props.action === "create"
        ? emit("submit", message)
        : emit("get-resume", "view");

      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Данные успешно обновлены"
      );
      Object.keys(resumeForm.value.form).forEach((key) => {
        delete resumeForm.value.form[key as keyof typeof resumeForm.value.form];
      });
    } catch (error) {
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Возникла ошибка ${error}`
      );
    }
  },
});
</script>

<template>
  <div class="py-3">
    <form
      @submit.prevent="resumeForm.submitResume"
      class="form form-check"
      role="form"
    >
      <LabelSlot :label="'Регион'">
        <SelectInput
          :name="'region_id'"
          :select="storeClassify.classData.regions"
          v-model="resumeForm.form['region_id']"
        />
      </LabelSlot>
      <LabelSlot :label="'Фамилия'">
        <InputElement
          :isneed="true"
          :name="'surname'"
          :place="'Фамилия*'"
          :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
          v-model="resumeForm.form['surname']"
        />
      </LabelSlot>
      <LabelSlot :label="'Имя'">
        <InputElement
          :isneed="true"
          :name="'firstname'"
          :place="'Имя*'"
          :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
          v-model="resumeForm.form['firstname']"
        />
      </LabelSlot>
      <LabelSlot :label="'Отчество'">
        <InputElement
          :name="'patronymic'"
          :place="'Отчество'"
          v-model="resumeForm.form['patronymic']"
        />
      </LabelSlot>
      <LabelSlot :label="'Изменение имени'">
        <InputElement
          :name="'previous'"
          :place="'Изменение имени'"
          v-model="resumeForm.form['previous']"
        />
      </LabelSlot>
      <LabelSlot :label="'Дата рождения*'">
        <InputElement
          :isneed="true"
          :name="'birthday'"
          :place="'Дата рождения*'"
          :typeof="'date'"
          v-model="resumeForm.form['birthday']"
        />
      </LabelSlot>
      <LabelSlot :label="'Место рождения'">
        <InputElement
          :name="'birthplace'"
          :place="'Место рождения'"
          v-model="resumeForm.form['birthplace']"
        />
      </LabelSlot>
      <LabelSlot :label="'Гражданство'">
        <InputElement
          :name="'country'"
          :place="'Гражданство'"
          v-model="resumeForm.form['country']"
        />
      </LabelSlot>
      <LabelSlot :label="'Двойное гражданство'">
        <InputElement
          :name="'ext_country'"
          :place="'Двойное гражданство'"
          v-model="resumeForm.form['ext_country']"
        />
      </LabelSlot>
      <LabelSlot :label="'СНИЛС'">
        <InputElement
          :name="'snils'"
          :place="'СНИЛС'"
          :pattern="'[0-9]{11}'"
          v-model="resumeForm.form['snils']"
        />
      </LabelSlot>
      <LabelSlot :label="'ИНН'">
        <InputElement
          :name="'inn'"
          :place="'ИНН'"
          :max="'12'"
          :pattern="'[0-9]{12}'"
          v-model="resumeForm.form['inn']"
        />
      </LabelSlot>
      <LabelSlot :label="'Семейное положение'">
        <InputElement
          :name="'marital'"
          :place="'Семейное положение'"
          v-model="resumeForm.form['marital']"
        />
      </LabelSlot>
      <LabelSlot :label="'Образование'">
        <TextArea
          :name="'education'"
          :place="'Образование'"
          v-model="props.resume['education']"
        />
      </LabelSlot>
      <LabelSlot :label="'Дополнительно'">
        <TextArea
          :name="'addition'"
          :place="'Дополнительно'"
          v-model="props.resume['addition']"
        />
      </LabelSlot>
      <BtnGroup>
        <GroupContent :cancel-needs="false" />
        <router-link
          v-if="props.action === 'create'"
          class="btn btn-outline-danger"
          type="button"
          :to="{ name: 'persons' }"
        >
          Отмена
        </router-link>
        <button
          v-if="props.action === 'update'"
          class="btn btn-outline-danger"
          type="button"
          @click="emit('cancel')"
        >
          Отмена
        </button>
      </BtnGroup>
    </form>
  </div>
</template>
