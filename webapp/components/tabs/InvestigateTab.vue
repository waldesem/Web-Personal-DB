<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const inquisition = ref(<Inquisition>{});

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
    <FormsInvestigationForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.investigations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.investigations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="border rounded p-3"
    >
      <FormsInvestigationForm
        v-if="edit && itemId == item['id'].toString()"
        :investigation="inquisition"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions &&
              idx &&
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            @delete="
              anketaState.deleteItem(item['id'].toString(), 'investigations')
            "
            @update="
              inquisition = item;
              itemId = item['id'].toString();
              edit = true;
            "
          >
            <FormsFileForm
              :accept="'*'"
              @submit="
                anketaState.submitFile(
                  $event,
                  'investigations',
                  anketaState.share.value.candId
                )
              "
            />
          </ElementsActionIcons>
        </ElementsLabelSlot>
        <p class="text-primary">
          {{ "Расследование/Проверка #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Тема проверки'">{{
          item["theme"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Информация'">{{
          item["info"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{
          item["username"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
  <p class="text-primary">Расследования/Проверки не проводились</p>
  </div>
</template>
