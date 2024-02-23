<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

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
  staff: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
});

const staffForm = ref({
  form: <Record<string, any>>{},

  updateItem: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/staff/${props.candId}`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/staff/${props.itemId}`,
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
</script>

<template>
  <form
    @submit.prevent="staffForm.updateItem;"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'position'"
      :label="'Должность'"
      :need="true"
      :model="props.staff['position']"
      @input-event="staffForm.form['position'] = $event.target.value"
    />
    <TextLabel
      :name="'department'"
      :label="'Подраздление'"
      :model="props.staff['department']"
      @input-event="staffForm.form['department'] = $event.target.value"
    />

    <BtnGroupForm>
      <button
        class="btn btn-outline-primary btn-md"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button class="btn btn-outline-primary btn-md" name="reset" type="reset">
        Очистить
      </button>
    </BtnGroupForm>
  </form>
</template>
