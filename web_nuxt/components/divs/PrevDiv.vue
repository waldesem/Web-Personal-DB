<script setup lang="ts">
import type { Previous } from "@/types";

prefetchComponents("FormsPreviousForm");

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

const collapse = ref(false);
const pending = ref(false);
const edit = ref(false);
const itemId = ref("");
const prev = ref({} as Previous);
const previous = ref<Previous[]>([]);

const { refresh, status } = await useLazyAsyncData("previous", async () => {
  previous.value = await authFetch("/route/items/previous/" + props.candId) as Previous[];
});

async function submitPrevious(form: Previous) {
  closeAction();  
  pending.value = true;
  const { message } = await authFetch(`/route/items/previous/${props.candId}`, {
    method: "POST",
    body: form,
  }) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deletePrevious(id: string, idx: integer) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/previous/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    previous.value.splice(idx, 1);
  };
  emit("message", message);
}

function cancelOperation() {
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
    :disabled="status == 'pending' || pending"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsPreviousForm
          @cancel="cancelOperation"
          @update="submitPrevious"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="previous && previous.length">
    <div v-for="(item, idx) in previous" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
      <ElementsCardDiv v-else>
        <FormsPreviousForm
          v-if="edit && itemId == item['id'].toString()"
          :previous="prev"
          @cancel="cancelOperation"
          @update="submitPrevious"
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
          <ElementsNavSimpHoriz
            @delete="deletePrevious(item['id'], idx)"
            @update="
              prev = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
