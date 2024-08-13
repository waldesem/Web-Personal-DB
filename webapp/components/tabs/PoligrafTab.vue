<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />  
  <div v-if="collapse" class="border rounded p-3">
    <FormsPoligrafForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.poligrafs.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.poligrafs"
      :key="idx"
      class="border rounded p-3"
    >
      <FormsPoligrafForm
        v-if="edit && itemId == item['id'].toString()"
        :poligraf="poligraf"
        @cancel="cancelAction"
      />
      <div v-else>
        <p class="text-primary">
          {{ "Обследование на полиграфе #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Тема проверки'">{{ item["theme"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Результат'">{{ item["results"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{ item["username"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsNaviHorizontal
          v-show="
            !idx &&
            anketaState.anketa.value.persons['user_id'] ==
              userState.user.value.userId &&
            anketaState.anketa.value.persons['standing']
          "
          @update="
            poligraf = item;
            itemId = item['id'].toString();
            edit = true;
          "
          @delete="anketaState.deleteItem(item['id'].toString(), 'poligrafs')"
          @upload="openFileForm('poligraf-file')"
        />
        <div v-show="false">
          <UInput
            id="poligraf-file"
            type="file"
            accept="*"
            multiple
            @change="
              anketaState.submitFile(
                $event,
                'poligrafs',
                anketaState.share.value.candId
              )
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
  <p class="text-primary">Обследование на полиграфе не проводилось</p>
  </div>
</template>
