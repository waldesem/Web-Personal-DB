<script setup lang="ts">
import type { Pfo } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const authFetch = useFetchAuth();

const toast = useToast();

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
const collapse = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);

const {
  data: poligrafs,
  refresh,
  status,
} = await useLazyAsyncData("poligrafs", async () => {
  const response = await authFetch('/api/poligrafs/' + props.candId);
  return response  as Pfo[];
});

async function deletePoligraf(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch('/api/poligrafs/' + id, {
    method: "DELETE",
  });
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  refresh();
}

async function cancelOperation() {
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
    :label="collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsPoligrafForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="poligrafs && poligrafs.length">
    <div
      v-for="(item, index) in poligrafs"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="4" />
      <UCard v-else>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Обследование на полиграфе ID #" + item["id"] }}
          </div>
        </template>
        <FormsPoligrafForm
          v-if="edit && itemId == item['id'].toString()"
          :poligraf="poligraf"
          @cancel="cancelOperation"
          @update="refresh"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тема проверки'">{{
            item["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Результат'">{{
            item["results"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :cand-id="props.candId"
            :input-id="'poligrafs-file'"
            :item="'poligrafs'"
            @update="
              poligraf = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deletePoligraf(item['id'])"
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="4" />
    <p v-else class="text-red-800">Обследование на полиграфе не проводилось</p>
  </div>
</template>
