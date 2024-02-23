<script setup lang="ts">
import { defineAsyncComponent, ref, computed } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
)
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
  contact: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
});

const contactForm = ref({
  form: <Record<string, any>>{},
  selected_item: {
    phone: "Телефон",
    email: "E-mail",
    other: "Другое",
  },

  updateItem: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/contact/${props.candId}`,
              this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/contact/${props.itemId}`,
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

const view = computed(() => {
  if (contactForm.value.form["view"] === "Телефон") {
    return "tel";
  } else if (contactForm.value.form["view"] === "E-mail") {
    return "email";
  } else {
    return "text";
  }
});
</script>

<template>
  <form
    @submit.prevent="contactForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Выбрать'"
      :select="contactForm.selected_item"
      :model="props.contact['view']"
      @input-event="contactForm.form['view'] = $event.target.value"
    />
    <InputLabel
      :name="'contact'"
      :label="'Контакт'"
      :typeof="view"
      :need="true"
      :model="props.contact['contact']"
      @input-event="
        contactForm.form['contact'] = $event.target.value
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
