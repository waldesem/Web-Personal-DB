<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const anketaState = stateAnketa();

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
const items = computed(() =>
  anketaState.anketa.value.inquiries.map((item) => {
    return {
      label: "Результат обследования ID #" + item["id"],
    };
  })
);

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
        <FormsPoligrafForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.poligrafs.length">
    <UAccordion :items="items" size="lg" multiple>
      <template #item="{ index }">
        <div class="border rounded pt-3 pb-1 px-3">
          <FormsPoligrafForm
            v-if="
              edit &&
              itemId ==
                anketaState.anketa.value.poligrafs[index]['id'].toString()
            "
            :poligraf="poligraf"
            @cancel="cancelAction"
          />
          <div v-else>
            <ElementsLabelSlot :label="'Тема проверки'">{{
              anketaState.anketa.value.poligrafs[index]["theme"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Результат'">{{
              anketaState.anketa.value.poligrafs[index]["results"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Сотрудник'">{{
              anketaState.anketa.value.poligrafs[index]["username"]
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Дата записи'">
              {{
                new Date(
                  anketaState.anketa.value.poligrafs[index]["created"] + " UTC"
                ).toLocaleString("ru-RU")
              }}
            </ElementsLabelSlot>
            <ElementsNaviHorizont
              v-show="!index && editState"
              @update="
                poligraf = anketaState.anketa.value.poligrafs[index];
                itemId =
                  anketaState.anketa.value.poligrafs[index]['id'].toString();
                edit = true;
              "
              @delete="
                anketaState.deleteItem(
                  anketaState.anketa.value.poligrafs[index]['id'].toString(),
                  'poligrafs'
                )
              "
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
      </template>
    </UAccordion>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Обследование на полиграфе не проводилось</p>
  </div>
</template>

