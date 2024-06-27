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
  const collapsePoligraf = document.getElementById("poligraf");
  collapsePoligraf?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <div class="collapse card card-body mb-3" id="poligraf">
    <PoligrafForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.poligrafs.length">
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
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Обследование на полиграфе #" + (idx+1) }}
        </p>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"]).toLocaleString("ru-RU") + ' UTC' }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Обследование на полиграфе не проводилось</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>