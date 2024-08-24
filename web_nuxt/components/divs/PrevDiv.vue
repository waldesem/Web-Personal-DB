<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Previous } from "@/utils/interfaces";

const anketaState = stateAnketa();

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
    v-if="edit"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
        <FormsPreviousForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.previous.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.previous"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
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
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

