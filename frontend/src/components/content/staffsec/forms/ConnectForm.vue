<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { server } from "@utilities/utils";

const InputSmall = defineAsyncComponent(
  () => import("@components/elements/InputSmall.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

const props = defineProps({
  id: String,
  page: Number,
  action: String,
  companies: Array,
  cities: Array,
  item: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getContacts: {
    type: Function,
    required: true,
  },
});

const emit = defineEmits(["deactivate"]);

const contactForm = ref({
  form: <Record<string, any>>{},

  updateContact: async function (): Promise<void> {
    try {
      const response =
        props.action === "create"
          ? await storeAuth.axiosInstance.post(
            `${server}/connect`, 
            this.form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/connect/${props.id}`,
              this.form
            );
      console.log(response.status);

      const alert = {
        create: ["alert-success", "Контакт добавлен"],
        edit: ["alert-info", "Контакт обновлен"],
      };
      storeAlert.alertMessage.setAlert(
        alert[props.action as keyof typeof alert][0],
        alert[props.action as keyof typeof alert][1]
      );
      props.getContacts(props.page);
      Object.keys(this.form).forEach((key) => {
        delete this.form[key as keyof typeof this.form];
      });
      emit("deactivate");
    } catch (error) {
      console.log(error);
    }
  },
});
</script>

<template>
  <form @submit.prevent="contactForm.updateContact" class="form form-check">
    <InputSmall
      :name="'company'"
      place="Организация"
      :need="true"
      :lst="'companies'"
      :selects="props.companies"
      :model="item.form['company']"
      @input-event="contactForm.form['company'] = $event.target.value"
    />
    <InputSmall
      :name="'city'"
      place="Город"
      :need="true"
      :lst="'cities'"
      :selects="props.cities"
      :model="item.form['city']"
      @input-event="contactForm.form['city'] = $event.target.value"
    />
    <InputSmall
      :name="'fullname'"
      place="Имя"
      :need="true"
      :model="item.form['fullname']"
      @input-event="contactForm.form['fullname'] = $event.target.value"
    />
    <InputSmall
      :name="'phone'"
      place="Телефон"
      :model="item.form['phone']"
      @input-event="contactForm.form['phone'] = $event.target.value"
    />
    <InputSmall
      :name="'adding'"
      place="Добав"
      :model="item.form['adding']"
      @input-event="contactForm.form['adding'] = $event.target.value"
    />
    <InputSmall
      :name="'mobile'"
      place="Мобильный"
      :model="item.form['mobile']"
      @input-event="contactForm.form['mobile'] = $event.target.value"
    />
    <InputSmall
      :name="'mail'"
      place="Почта"
      :model="item.form['mail']"
      @input-event="contactForm.form['mail'] = $event.target.value"
    />
    <InputSmall
      :name="'comment'"
      place="Комментарий"
      :model="item.form['comment']"
      @input-event="contactForm.form['comment'] = $event.target.value"
    />
    <BtnGroupForm>
      <button
        class="btn btn-outline-primary btn-sm"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button
        class="btn btn-outline-primary btn-sm"
        name="reset"
        type="reset"
      >
        Очистить
      </button>
    </BtnGroupForm>
  </form>
</template>
@/store/auth