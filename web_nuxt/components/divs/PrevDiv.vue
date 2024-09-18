<script setup lang="ts">
import type { Previous } from "@/types/interfaces";

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
const previous = ref({} as Previous);

const {
  data: previous,
  refresh,
  status,
} = await useLazyAsyncData("previous", async () => {
  const response = await authFetch("/api/previous/" + props.candId);
  return response;
});

async function deletePrevious(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch("/api/previous/" + id, {
    method: "DELETE",
  });
  console.log(response);
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
        <FormsPreviousForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="previous && previous.length">
    <div v-for="(item, idx) in previous" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="4" />
      <UCard v-else>
        <FormsPreviousForm
          v-if="edit && itemId == item['id'].toString()"
          :previous="previous"
          @cancel="cancelOperation"
          @update="refresh"
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
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deletePrevious(item['id'].toString())"
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
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="4" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
