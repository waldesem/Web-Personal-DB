<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
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

const emit = defineEmits(["get-resume"]);

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
  form: <Resume>{},

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
        :name="'category'"
        :label="'Категория'"
        :select="storeClassify.classData.category"
        @input-event="
          resumeForm.form['category_id'] = $event.target.value
        "
        :model="props.resume['category_id']"
      />
      <SelectDiv
        :name="'region_id'"
        :label="'Регион'"
        :select="storeClassify.classData.regions"
        @input-event="
          resumeForm.form['region_id'] = $event.target.value
        "
        :model="props.resume['region_id']"
      />
      <InputLabel
        :isneed="true"
        :name="'fullname'"
        :label="'Полное ФИО*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        @input-event="
          resumeForm.form['fullname'] = $event.target.value.toUpperCase()
        "
        :model="props.resume['fullname']"
      />
      <TextLabel
        :name="'previous'"
        :label="'Изменение имени'"
        @input-event="
          resumeForm.form['previous'] = $event.target.value
        "
        :model="props.resume['previous']"
      />
      <InputLabel
        :isneed="true"
        :name="'birthday'"
        :label="'Дата рождения*'"
        :typeof="'date'"
        @input-event="
          resumeForm.form['birthday'] = $event.target.value
        "
        :model="props.resume['previous']"
      />
      <TextLabel
        :name="'birthplace'"
        :label="'Место рождения'"
        @input-event="
          resumeForm.form['birthplace'] = $event.target.value
        "
        :model="props.resume['birthplace']"
      />
      <InputLabel
        :name="'country'"
        :label="'Гражданство'"
        :max="'255'"
        @input-event="
          resumeForm.form['country'] = $event.target.value
        "
        :model="props.resume['country']"
      />
      <InputLabel
        :name="'ext_country'"
        :label="'Двойное гражданство'"
        :max="'255'"
        @input-event="
          resumeForm.form['ext_country'] = $event.target.value
        "
        :model="props.resume['ext_country']"
      />
      <InputLabel
        :name="'snils'"
        :label="'СНИЛС'"
        :pattern="'[0-9]{11}'"
        @input-event="
          resumeForm.form['snils'] = $event.target.value
        "
        :model="props.resume['snils']"
      />
      <InputLabel
        :name="'inn'"
        :label="'ИНН'"
        :max="'12'"
        :pattern="'[0-9]{12}'"
        @input-event="
          resumeForm.form['inn'] = $event.target.value
        "
        :model="props.resume['inn']"
      />
      <TextLabel
        :name="'education'"
        :label="'Образование'"
        @input-event="
          resumeForm.form['education'] = $event.target.value
        "
        :model="props.resume['education']"
      />
      <InputLabel
        :name="'marital'"
        :label="'Семейнное положение'"
        :max="'255'"
        @input-event="
          resumeForm.form['marital'] = $event.target.value
        "
        :model="props.resume['marital']"
      />
      <TextLabel
        :name="'addition'"
        :label="'Дополнительно'"
        @input-event="
          resumeForm.form['addition'] = $event.target.value
        "
        :model="props.resume['addition']"
      />

      <BtnGroup>
        <button 
          class="btn btn-outline-primary" 
          data-bs-dismiss="modal"
          type="submit">
          Принять
        </button>
        <button class="btn btn-outline-primary" type="reset">Очистить</button>
        <router-link
          v-if="props.action === 'create'"
          class="btn btn-outline-primary"
          type="button"
          :to="{ name: 'persons' }"
        >
          Отмена
        </router-link>
      </BtnGroup>
    </form>
  </div>
</template>
