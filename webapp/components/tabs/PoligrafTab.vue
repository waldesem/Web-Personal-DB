<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

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
    <FormsPoligrafForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.poligrafs.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.poligrafs"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsPoligrafForm
        v-if="edit && itemId == item['id'].toString()"
        :poligraf="poligraf"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions && idx &&
              anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            @delete="anketaState.deleteItem(item['id'].toString(), 'poligrafs')"
            @update="
              poligraf = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :for-input="'poligrafs-file'"
          >
            <FormsFileForm
              v-show="actions"
              :name-id="'poligrafs-file'"
              :accept="'*'"
              @submit="
                anketaState.submitFile(
                  $event,
                  'poligrafs',
                  anketaState.share.value.candId
                )
              "
            />
          </ElementsActionIcons>
        </ElementsLabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Обследование на полиграфе #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Тема проверки'">{{ item["theme"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Результат'">{{ item["results"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{ item["username"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
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
