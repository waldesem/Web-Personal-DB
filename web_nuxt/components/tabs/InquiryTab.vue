<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const need = ref({} as Needs);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

const items = computed(() =>
  anketaState.anketa.value.inquiries.map((item, index) => {
    return {
      label: "Запрос о сотруднике ID #" + item["id"],
      defaultOpen: index === 0,
    };
  })
);
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
        <FormsInquiryForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.inquiries.length">
    <UAccordion :items="items" size="lg" multiple>
      <template #item="{ index }">
        <div class="border rounded pt-3 pb-1 px-3">
          <FormsInquiryForm
            v-if="
              edit &&
              itemId ==
                anketaState.anketa.value.inquiries[index]['id'].toString()
            "
            :inquiry="need"
            @cancel="cancelAction"
          />
          <div v-else>
            <ElementsLabelSlot :label="'Информация'">{{
              anketaState.anketa.value.inquiries[index]["info"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Иннициатор'">{{
              anketaState.anketa.value.inquiries[index]["origins"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Сотрудник'">{{
              anketaState.anketa.value.inquiries[index]["username"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Дата записи'">
              {{
                new Date(
                  anketaState.anketa.value.inquiries[index]["created"] + " UTC"
                ).toLocaleString("ru-RU")
              }}
            </ElementsLabelSlot>
            <ElementsNaviHorizontal
              v-show="
                !index &&
                anketaState.anketa.value.persons['user_id'] ==
                  userState.user.value.userId &&
                anketaState.anketa.value.persons['editable']
              "
              :last-index="2"
              @delete="
                anketaState.deleteItem(
                  anketaState.anketa.value.inquiries[index]['id'].toString(),
                  'inquiries'
                )
              "
              @update="
                need = anketaState.anketa.value.inquiries[index];
                itemId =
                  anketaState.anketa.value.inquiries[index]['id'].toString();
                edit = true;
              "
            />
          </div>
        </div>
      </template>
    </UAccordion>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Запросы о сотруднике не поступали</p>
  </div>
</template>

