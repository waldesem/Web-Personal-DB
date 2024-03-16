<script setup lang="ts">
import { defineAsyncComponent, ref, computed } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";
import { router } from "@/router/router";

const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);
const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore();

const emit = defineEmits(["get-resume", "cancel"]);

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
              `${server}/resume/${props.resume['id']}`,
              this.form
            );

      const { message } = response.data;

      props.action == "create" 
        ? router.push({ name: "profile", params: { id: message } })
        : emit("get-resume", "view");
      
      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Данные успешно обновлены"
      );
    } catch (error) {
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Возникла ошибка ${error}`
      );
    }
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
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
      <SelectDiv
        :name="'region_id'"
        :label="'Регион'"
        :select="storeClassify.classData.regions"
        v-model="resumeForm.form['region_id']"
      />
      <InputLabel
        :isneed="true"
        :name="'surname'"
        :label="'Фамилия*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm.form['surname']"
      />
      <InputLabel
        :isneed="true"
        :name="'firstname'"
        :label="'Имя*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm.form['firstname']"
      />
      <InputLabel
        :isneed="true"
        :name="'patronymic'"
        :label="'Отчество*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm.form['patronymic']"
      />
      <InputLabel
        :name="'previous'"
        :label="'Изменение имени*'"
        :max="'255'"
        v-model="resumeForm.form['previous']"
      />
      <InputLabel
        :isneed="true"
        :name="'birthday'"
        :label="'Дата рождения*'"
        :typeof="'date'"
        v-model="resumeForm.form['previous']"
      />
      <InputLabel
        :name="'birthplace'"
        :label="'Место рождения'"
        :max="'255'"
        v-model="resumeForm.form['birthplace']"
      />
      <InputLabel
        :name="'country'"
        :label="'Гражданство'"
        :max="'255'"
        v-model="resumeForm.form['country']"
      />
      <InputLabel
        :name="'ext_country'"
        :label="'Двойное гражданство'"
        :max="'255'"
        v-model="resumeForm.form['ext_country']"
      />
      <InputLabel
        :name="'snils'"
        :label="'СНИЛС'"
        :pattern="'[0-9]{11}'"
        v-model="resumeForm.form['snils']"
      />
      <InputLabel
        :name="'inn'"
        :label="'ИНН'"
        :max="'12'"
        :pattern="'[0-9]{12}'"
        v-model="resumeForm.form['inn']"
      />
      <InputLabel
        :name="'marital'"
        :label="'Семейнное положение'"
        :max="'255'"
        v-model="resumeForm.form['marital']"
      />
      <TextLabel
        :name="'education'"
        :label="'Образование'"
        v-model="props.resume['education']"
      />
      <TextLabel
        :name="'addition'"
        :label="'Дополнительно'"
        v-model="props.resume['addition']"
      />
      <BtnGroup>
        <button 
          class="btn btn-outline-primary" 
          type="submit">
          Принять
        </button>
        <button class="btn btn-outline-secondary" type="reset">Очистить</button>
        <router-link
          v-if="props.action === 'create'"
          class="btn btn-outline-warning"
          type="button"
          :to="{ name: 'persons' }"
        >
          Отмена
        </router-link>
        <button v-if="props.action === 'update'"
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
