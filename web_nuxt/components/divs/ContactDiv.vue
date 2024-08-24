<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Contact } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const contact = ref({} as Contact);

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
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
        <FormsContactForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.contacts.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.contacts"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsContactForm
          v-if="edit && itemId == item['id'].toString()"
          :contact="contact"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Вид'">{{ item["view"] }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Контакт'">{{
            item["contact"]
          }}</ElementsLabelSlot>
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'contacts')"
            @update="
              contact = item;
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

