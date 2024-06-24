<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Pfo } from "@/interfaces";
import { stateAnketa, submitFile } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const PoligrafForm = defineAsyncComponent(
  () => import("@components/content/forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  tabAction: {
    type: String,
    default: "",
  },
  currentTab: {
    type: String,
    default: "",
  },
});

const poligraf = ref({
  itemId: "",
  item: <Pfo>{},
  showActions: false,
});

function cancelAction() {
  poligraf.value.itemId = "";
  Object.keys(poligraf.value.item).forEach(
    (key) => delete poligraf.value.item[key as keyof typeof poligraf.value.item]
  );
  emit("cancel");
}

function submitForm(form: Object) {
  stateAnketa.updateItem("poligrafs", form);
  cancelAction();
}
</script>

<template>
  <PoligrafForm
    v-if="props.tabAction === 'create' && props.currentTab === 'PoligrafTab'"
    @submit="submitForm"
    @cancel="emit('cancel')"
  />
  <div v-else-if="stateAnketa.anketa.poligrafs.length" class="py-3">
    <div
      v-for="(item, idx) in stateAnketa.anketa.poligrafs"
      :key="idx"
      @mouseover="poligraf.showActions = true"
      @mouseout="poligraf.showActions = false"
      class="card card-body mb-3"
    >
      <PoligrafForm
        v-if="poligraf.itemId === item['id'].toString()"
        :poligraf="poligraf.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="poligraf.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'poligrafs')"
            @update="
              poligraf.item = item;
              poligraf.itemId = item['id'].toString();
            "
            :for-input="'poligrafs-file'"
          >
            <FileForm
              v-show="poligraf.showActions"
              :name-id="'poligrafs-file'"
              :accept="'*'"
              @submit="submitFile($event, 'poligrafs')"
            />
          </ActionIcons>
        </LabelSlot>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(String(item["created"])).toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
