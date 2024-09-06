<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Previous } from "@/utils/interfaces";

const anketaState = stateAnketa();

await anketaState.getItem('previous');

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const previous = ref({} as Previous);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

const editState = inject("editState") as boolean
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
        <FormsPreviousForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.previous.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.previous"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsPreviousForm
          v-if="edit && itemId == item['id'].toString()"
          :previous="previous"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Фамилия'">
            {{ item["surname"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Имя'">
            {{ item["firstname"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['patronymic']" :label="'Отчество'">
            {{ item["patronymic"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['changed']" :label="'Год изменения'">
            {{ item["changed"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['reason']" :label="'Причина'">
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
            @delete="anketaState.deleteItem(item['id'].toString(), 'previous')"
            @update="
              previous = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

