<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";

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
  investigation: {
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

const investigationForm = ref({
  form: <Record<string, any>>{},

  updateItem: function () {
    const itemId = props.action === "create" ? props.candId : props.itemId;
    props.updateItem(props.action, "check", itemId, investigationForm.value.form);

    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
   },
});
</script>

<template>
  <form
    @submit.prevent="investigationForm.updateItem"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'theme'"
      :label="'Тема проверки'"
      :need="true"
      :model="props.investigation['theme']"
      @input-event="
        investigationForm.form['theme'] = $event.target.value
      "
    />
    <TextLabel
      :name="'info'"
      :label="'Информация'"
      :model="props.investigation['info']"
      @input-event="investigationForm.form['info'] = $event.target.value"
    />
    <BtnGroupForm>
      <button class="btn btn-outline-primary" type="submit">Принять</button>
      <button class="btn btn-outline-primary" type="reset">Очистить</button>
      <button
        class="btn btn-outline-primary"
        type="button"
        @click="emit('deactivate')"
      >
        Отмена
      </button>
    </BtnGroupForm>
  </form>
</template>
