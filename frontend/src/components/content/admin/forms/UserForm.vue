<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const props = defineProps({
  action: String,
  item: {
    type: Object as () => Record<string, any>,
    default: {},
  },
  userAction: {
    type: Function,
    default: () => {},
  },
  getUsers: {
    type: Function,
    default: () => {},
  },
});

const emit = defineEmits(["deactivate"]);

const userForm = ref({
  form: <Record<string, any>>{},
  submitUser: async function (): Promise<void> {
    try {
      const response =
        props.action === "edit"
          ? await storeAuth.axiosInstance.patch(`${server}/user`, this.form)
          : await storeAuth.axiosInstance.post(`${server}/user`, this.form);

        const { message } = response.data;
      if (message === "Changed") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь успешно изменен"
        );
        props.userAction("view");
      } else {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь успешно создан"
        );
        props.getUsers();
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        "Ошибка сохранения данных"
      );
    }
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
  },
})
</script>

<template>
  <ModalWin
    :title="
      props.action === 'edit'
        ? 'Изменить пользователя'
        : 'Создать пользователя'
    "
    :size="'modal-xl'"
    :id="'modalUser'"
  >
    <form
      @submit.prevent="userForm.submitUser"
      class="form form-check"
      role="form"
    >
      <InputLabel
        :name="'fullname'"
        :label="'Имя пользователя'"
        :need="true"
        :pattern="'[a-zA-Zа-яА-Я ]+'"
        @input-event="
          userForm.form['fullname'] = $event.target.value
        "
        :model="props.item['fullname']"
      />
      <InputLabel
        :name="'username'"
        :label="'Учетная запись'"
        :need="true"
        :pattern="'[a-zA-Z]+'"
        :disable="props.action === 'edit'"
        @input-event="
          userForm.form['username'] = $event.target.value
        "
        :model="props.item['username']"
      />
      <InputLabel
        :name="'email'"
        :label="'Электронная почта'"
        :need="true"
        :typeof="'email'"
        @input-event="userForm.form['email'] = $event.target.value"
        :model="props.item['email']"
      />

      <BtnGroupForm>
        <button
          class="btn btn-outline-secondary"
          name="submit"
          type="submit"
          data-bs-dismiss="modal"
        >
          {{
            props.action === "create" ? "Создать" : "Изменить"
          }}
        </button>
        <button class="btn btn-outline-secondary" name="reset" type="reset">
          Очистить
        </button>
        <button
          class="btn btn-outline-secondary"
          name="cancel"
          type="button"
          data-bs-dismiss="modal"
          @click="emit('deactivate')"
        >
          Отмена
        </button>
      </BtnGroupForm>
    </form>
  </ModalWin>
</template>
