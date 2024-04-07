<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
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

onBeforeMount(() => {
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
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }
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
  poligraf.value.showActions = false;
}
</script>

<template>
  <div class="py-3">
    <ActionHeader
      :id="'poligraf'"
      :header="'Полиграф'"
      :action="poligraf.action"
      @action="poligraf.action = poligraf.action ? '' : 'create'"
    />
    <PoligrafForm
      v-if="poligraf.action"
      :poligraf="poligraf.item"
      @submit="submitForm"
      @cancel="poligraf.action = ''; poligraf.showActions = false"
    />
    <div v-else
     @mouseover="poligraf.handleMouse"
     @mouseout="poligraf.handleMouse"
    >
      <div v-if="props.poligrafs.length" class="collapse" id="poligraf"> 
        <div class="mb-3" v-for="(item, idx) in props.poligrafs" :key="idx">
          <div class="card card-body">
            <LabelSlot v-show="poligraf.showActions">
              <ActionIcons
                @delete="emit('delete', item['id'].toString(), 'poligraf')"
                @update="
                  poligraf.action = 'update';
                  poligraf.item = item;
                  poligraf.itemId = item['id'].toString();
                "
              />
            </LabelSlot>
            <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
            <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
            <LabelSlot :label="'Дата'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
          </div>
          <FileForm :accept="'*'" @submit="emit('file')" />
        </div>
      </div>
      <p v-else>Данные отсутствуют</p>
    </div>
  </div>
</template>
