<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Staff } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["deactivate", "submit"]);

const props = defineProps({
  candId: String,
  itemId: String,
  action: String,
  staff: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const staffForm = ref({
  form: <Staff>{},

  updateItem: function () {
    const itemId = props.action === "create" ? props.candId : props.itemId;
    emit("submit", [itemId, staffForm.value.form]);

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
