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
  poligraf: {
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

const poligrafForm = ref({
  form: <Record<string, any>>{},
  selected_item: {
    candidate: "Проверка кандидата",
    check: "Служебная проверка",
    investigation: "Служебное расследование",
  },

  updateItem: function () {
    const itemId = props.action === "create" ? props.candId : props.itemId;
    props.updateItem(props.action, "check", itemId, poligrafForm.value.form);

    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
   },
});
</script>

<template>
  <form
    @submit.prevent="poligrafForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'theme'"
      :label="'Тема проверки'"
      :select="poligrafForm.selected_item"
      :model="props.poligraf['theme']"
      @input-event="
        poligrafForm.form['theme'] = $event.target.value
      "
    />
    <TextLabel
      :name="'results'"
      :label="'Результат'"
      :model="props.poligraf['results']"
      @input-event="
        poligrafForm.form['results'] = $event.target.value
      "
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
