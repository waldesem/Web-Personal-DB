<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);
const storeAuth = authStore();
const storeAlert = alertStore();

const emit = defineEmits(["deactivate"]);

const props = defineProps({
  candId: String,
  itemId: String,
  action: String,
  resume: {
    type: Object as () => Record<string, any>,
    default: {},
  },
  getItem: {
    type: Function,
    default: () => {},
  },
});

const resumeForm = ref({
  form: <Record<string, any>>{},

  submitResume: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/resume`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/resume/${props.candId}`,
              this.form
            );

      console.log(response.status);

      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Данные успешно обновлены"
      );
      props.getItem();
    } catch (error) {
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Возникла ошибка ${error}`
      );
    }
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
   },
});

const select_items = {
  candidate: "Кандидат",
  suspict: "Проверяемый",
};
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
        :select="select_items"
        @input-event="
          resumeForm.form['category'] = $event.target.value
        "
        :model="props.resume['category']"
      />
      <InputLabel
        :isneed="true"
        :name="'fullname'"
        :label="'Полное ФИО*'"
        @input-event="
          resumeForm.form['fullname'] = $event.target.value
        "
        :model="props.resume['fullname'].toUpperCase()"
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

      <BtnGroupForm>
        <button class="btn btn-outline-primary" type="submit">Принять</button>
        <button class="btn btn-outline-primary" type="reset">Очистить</button>
        <router-link
          v-if="props.action === 'create'"
          class="btn btn-outline-primary"
          type="button"
          :to="{ name: 'persons' }"
        >
          Отмена
        </router-link>
        <button
          v-else
          class="btn btn-outline-primary"
          type="button"
          @click="emit('deactivate')"
        >
          Отмена
        </button>
      </BtnGroupForm>
    </form>
  </div>
</template>
@/store/auth