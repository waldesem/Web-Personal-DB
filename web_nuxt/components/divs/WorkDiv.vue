<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Work } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const workplace = ref({} as Work);

const { refresh } = await useLazyAsyncData("workplaces", async () => {
  await anketaState.getItem('workplaces');
})

async function updateWork(workForm: Work) {
  closeAction();
  Promise.all([
    await anketaState.updateItem("workplaces", workForm),
    await refresh()
  ])
}

async function deleteWork(index: string) {
  Promise.all([
    await anketaState.deleteItem(index, 'workplaces'),
    await refresh()
  ])
}

async function cancelOperation() {
  await refresh();
  closeAction();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="editState"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsWorkplaceForm 
        @cancel="cancelOperation" 
        @submit="updateWork"
      />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.workplaces.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.workplaces"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsWorkplaceForm
          v-if="edit && itemId == item['id'].toString()"
          :work="workplace"
          @cancel="cancelOperation"
          @submit="updateWork"
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
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="deleteWork(item['id'])"
            @update="
              workplace = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные о работе отсутствуют</p>
  </div>
</template>

