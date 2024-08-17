<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Pfo } from "@/interfaces";
import { stateAnketa, stateUser } from "@/state";

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

const actions = ref(false);
const edit = ref(false);
const itemId = ref("");
const poligraf = ref(<Pfo>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapsePoligraf = document.getElementById("clps_poligraf");
  collapsePoligraf?.setAttribute("class", "collapse card card-body");
}
</script>

<template>
  <div class="collapse card card-body mb-3" id="clps_poligraf">
    <PoligrafForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.poligrafs.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.poligrafs"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <PoligrafForm
        v-if="edit && itemId == item['id'].toString()"
        :poligraf="poligraf"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
              actions && idx &&
              stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
              stateAnketa.anketa.persons['standing']
            "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'poligrafs')"
            @update="
              poligraf = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :for-input="'poligrafs-file'"
          >
            <FileForm
              v-show="actions"
              :name-id="'poligrafs-file'"
              :accept="'*'"
              @submit="
                stateAnketa.submitFile(
                  $event,
                  'poligrafs',
                  stateAnketa.share.candId
                )
              "
            />
          </ActionIcons>
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Обследование на полиграфе #" + (idx + 1) }}
        </p>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["username"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
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
