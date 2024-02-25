<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["deactivate"]);

const props = defineProps({
  candId: String,
  itemId: String,
  action: String,
  work: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
});

const workForm = ref({
  form: <Record<string, any>>{},

  updateItem: function () {
    const itemId = props.action === "create" ? props.candId : props.itemId;
    props.updateItem(props.action, "workplace", itemId, workForm.value.form);

    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
   },
});
</script>

<template>
  <form
    @submit.prevent="workForm.updateItem"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'start_date'"
      :label="'Начало работы'"
      :typeof="'date'"
      :model="props.work['start_date']"
      @input-event="
        workForm.form['start_date'] = $event.target.value
      "
    />
    <InputLabel
      :name="'end_date'"
      :label="'Окончание работы'"
      :typeof="'date'"
      :model="props.work['end_date']"
      @input-event="
        workForm.form['end_date'] = $event.target.value
      "
    />
    <InputLabel
      :name="'workplace'"
      :label="'Место работы'"
      :need="true"
      :model="props.work['workplace']"
      @input-event="
        workForm.form['workplace'] = $event.target.value
      "
    />
    <TextLabel
      :name="'address'"
      :label="'Адрес организации'"
      :model="props.work['address']"
      @input-event="
        workForm.form['address'] = $event.target.value
      "
    />
    <TextLabel
      :name="'position'"
      :label="'Должность'"
      :model="props.work['position']"
      @input-event="
        workForm.form['position'] = $event.target.value
      "
    />
    <TextLabel
      :name="'reason'"
      :label="'Причина увольнения'"
      :model="props.work['reason']"
      @input-event="
        workForm.form['reason'] = $event.target.value
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
