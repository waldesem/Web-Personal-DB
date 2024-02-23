<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
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
  relation: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
});

const relationForm = ref({
  form: <Record<string, any>>{},

  updateItem: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/relation/${props.candId}`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/relation/${props.itemId}`,
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
    @submit.prevent="relationForm.updateItem"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'relation'"
      :label="'Тип связи'"
      :need="true"
      :model="props.relation['relation']"
      @input-event="
        relationForm.form['relation'] = $event.target.value
      "
    />
    <InputLabel
      :name="'relation_id'"
      :label="'ID связи'"
      :need="true"
      :model="props.relation['relation_id']"
      @input-event="
        relationForm.form['relation_id'] = $event.target.value
      "
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
