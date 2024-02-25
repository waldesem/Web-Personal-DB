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
  affils: {
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

const affilationForm = ref({
  form: <Record<string, any>>{},
  selected_item: {
    state: "Являлся государственным/муниципальным служащим",
    official: "Являлся государственным должностным лицом",
    relatives: "Связанные лица работают в государственных организациях",
    commercial: "Участвует в деятельности коммерческих организаций",
  },

  updateItem: function () {
    const itemId = props.action === "create" ? props.candId : props.itemId;
    props.updateItem(props.action, "affilation", itemId, affilationForm.value.form);

    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
    emit("deactivate");
   },
});
</script>

<template>
  <form
    @submit.prevent="affilationForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Тип участия'"
      :select="affilationForm.selected_item"
      :model="props.affils['view']"
      @input-event="affilationForm.form['view'] = $event.target.value"
    />
    <TextLabel
      :name="'name'"
      :label="'Организация'"
      :model="props.affils['name']"
      @input-event="affilationForm.form['name'] = $event.target.value"
    />
    <InputLabel
      :name="'inn'"
      :label="'ИНН'"
      :need="true"
      :model="props.affils['inn']"
      @input-event="affilationForm.form['inn'] = $event.target.value"
    />
    <TextLabel
      :name="'position'"
      :label="'Должность'"
      :model="props.affils['position']"
      @input-event="
        affilationForm.form['position'] = $event.target.value
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
      <button class="btn btn-outline-primary btn-md" type="reset">
        Очистить
      </button>
    </BtnGroupForm>
  </form>
</template>
