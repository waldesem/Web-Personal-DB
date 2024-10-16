<script setup lang="ts">
import type { Pfo } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

prefetchComponents(["FormsPoligrafForm", "ElementsSkeletonDiv"]);

const emit = defineEmits(["delete", "submit"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const edit = ref(false);
const pending = ref(false);
const collapse = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);
const poligrafs = ref<Pfo[]>([]);

const { refresh, status } = await useLazyAsyncData("poligrafs", async () => {
  poligrafs.value = await authFetch("/api/items/poligrafs/" + props.candId) as Pfo[];
});

async function submitPoligraf(form: Pfo) {
  closeAction();
  pending.value = true;
  await emit("submit", form, "poligrafs");
  pending.value = false;
  await refresh();
}

async function deletePoligraf(id: string) {
  closeAction();
  emit("delete", id, "poligrafs");
  await refresh();
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  collapse.value = false;
  edit.value = false;
  itemId.value = "";
}
</script>

<template>
  <UButton
    v-if="editable"
    class="py-3"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsPoligrafForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitPoligraf"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="poligrafs && poligrafs.length">
    <div
      v-for="(item, index) in poligrafs"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
      <ElementsCardDiv v-else>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Обследование на полиграфе ID #" + item["id"] }}
          </div>
        </template>
        <FormsPoligrafForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :poligraf="item"
          @cancel="cancelOperation"
          @update="submitPoligraf"
        />
        <div v-else>
          <ElementsLabelSlot v-if="item['theme']" :label="'Тема проверки'">{{
            item["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['results']" :label="'Результат'">{{
            item["results"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ useDateFormat(item["created"], "YYYY-MM-DD HH:mm:ss") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :cand-id="props.candId"
            :item="'poligrafs'"
            @update="
              poligraf = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deletePoligraf(item['id'])"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
    <p v-else class="text-red-800">Обследование на полиграфе не проводилось</p>
  </div>
</template>
