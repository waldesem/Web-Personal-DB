<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const PoligrafForm = defineAsyncComponent(
  () => import("@components/content/forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "poligraf");
});

const props = defineProps({
  poligrafs: {
    type: Array as () => Array<Pfo>,
    default: () => [],
  },
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Pfo>{},
});

function submitForm(form: Object) {
  emit(
    "submit",
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form
  );
  poligraf.value.action = "";
}

function submitFile(event: Event) {
  emit("file", event);
}
</script>

<template>
  <div class="py-3">
    <PoligrafForm
      v-if="poligraf.action"
      :poligraf="poligraf.item"
      @submit="submitForm"
      @cancel="poligraf.action = ''"
    />
    <div v-else>
      <div v-if="props.poligrafs.length">
        <CollapseDiv
          v-for="(item, idx) in props.poligrafs"
          :key="idx"
          :id="'poligraf' + idx"
          :idx="idx.toString()"
          :label="'Полиграф #' + (idx + 1)"
        >
          <LabelSlot :label="'Действия'">
            <ActionIcons
              @delete="emit('delete', item['id'].toString(), 'poligraf')"
              @update="
                poligraf.action = 'update';
                poligraf.item = item;
                poligraf.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
          <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
          <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
          <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
          <LabelSlot :label="'Дата'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelSlot>
        </CollapseDiv>
        <FileForm :accept="'*'" @submit="submitFile" />
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="poligraf.action = 'create'"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
