<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Work } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const workplace = ref({} as Work);

function cancelAction() {
  edit.value = false;
  collapse.value = false;
  itemId.value = "";
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <div v-if="collapse" class="p-1">
    <div class="border rounded p-3">
      <FormsWorkplaceForm @cancel="cancelAction" />
    </div>
  </div>
  <div v-if="anketaState.anketa.value.workplaces.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.workplaces"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsWorkplaceForm
          v-if="edit && itemId == item['id'].toString()"
          :work="workplace"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot v-if="item['now_work']" :label="'Текущая работа'">
            {{ item["now_work"] ? "Да" : "Нет" }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Начало работы'">
            {{ new Date(item["starts"]).toLocaleDateString("ru-RU") }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
            {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Место работы'">
            {{ item["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">
            {{ item["addresses"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Должность'">
            {{ item["position"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['reason']" :label="'Причина увольнения'">
            {{ item["reason"] }}
          </ElementsLabelSlot>
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'workplaces')"
            @update="
              workplace = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные о работе отсутствуют</p>
  </div>
</template>
