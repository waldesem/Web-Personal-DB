<script setup lang="ts">
import type { Affilation } from "@/types/interfaces";
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

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const affilation = ref({} as Affilation);

const {
  data: affilations,
  refresh,
  status,
} = await useLazyAsyncData("affilations", async () => {
  const response = await authFetch("/api/affilations/" + props.candId);
  return response as Affilation[];
});

async function deleteAffilation(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
 await authFetch("/api/affilations/" + id, {
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
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsAffilationForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="affilations && affilations.length">
    <div v-for="(item, idx) in affilations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
      <UCard v-else>
        <FormsAffilationForm
          v-if="edit && itemId == item['id'].toString()"
          :affils="affilation"
          @cancel="cancelOperation"
          @update="refresh"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип участия'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Организация'">{{
            item["organization"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'ИНН'">{{
            item["inn"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteAffilation(item['id'])"
            @update="
              affilation = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
