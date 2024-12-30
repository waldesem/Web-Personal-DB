<script setup lang="ts">
import type { Previous } from "@/types";

const emit = defineEmits(["message"]);

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

const modal = ref(false);
const pending = ref(false);
const prev = ref({} as Previous);
const previous = ref<Previous[]>([]);

const { refresh, status } = await useLazyAsyncData("previous", async () => {
  previous.value = (await authFetch(
    "/route/items/previous/" + props.candId
  )) as Previous[];
});

async function submitPrevious(form: Previous) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/previous/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  prev.value = {} as Previous;
  await refresh();
  emit("message", message);
}

async function deletePrevious(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/previous/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    previous.value.splice(idx, 1);
  }
  emit("message", message);
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :loading="status == 'pending' || pending"
    :label="
      status == 'pending' || pending
        ? 'Обновление данных...'
        : 'Добавить запись'
    "
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsPreviousForm
        :prev="prev"
        @cancel="prev = {}; modal = false"
        @update="submitPrevious"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in previous" :key="idx" class="p-1">
    <ElementsCardDiv>
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
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deletePrevious(item['id'], idx)"
          @update="
            prev = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
