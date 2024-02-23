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
  addrs: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
});

const addressForm = ref({
  form: <Record<string, any>>{},
  selected_item: {
    registration: "Адрес регистрации",
    live: "Адрес проживания",
    others: "Другое",
  },

  updateItem: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/address/${props.candId}`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/address/${props.itemId}`,
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
    @submit.prevent="addressForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="''"
      :label="''"
      :select="addressForm.selected_item"
      :model="props.addrs['view']"
      @input-event="addressForm.form['view'] = $event.target.value"
    />
    <InputLabel
      :name="'region'"
      :label="'Регион'"
      :need="true"
      :model="props.addrs['region']"
      @input-event="
        addressForm.form['region'] = $event.target.value
      "
    />
    <TextLabel
      :name="'address'"
      :label="'Полный адрес'"
      :model="props.addrs['address']"
      @input-event="
        addressForm.form['address'] = $event.target.value
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
