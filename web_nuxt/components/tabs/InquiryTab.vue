<script setup lang="ts">
import type { Needs } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

prefetchComponents(["FormsInquiryForm", "ElementsSkeletonDiv"]);

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
const need = ref({} as Needs);
const inquiries = ref<Needs[]>([]);

const { refresh, status } = await useLazyAsyncData("inquiries", async () => {
  inquiries.value = (await authFetch(
    `/api/items/inquiries/${props.candId}`
  )) as Needs[];
});

async function submitIquiry(form: Needs) {
  closeAction();
  pending.value = true;
  const { message } = (await authFetch(`/api/items/inquiries/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteNeed(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/api/items/inquiries/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  await refresh();
  emit("message", message);
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

function cancelOperation() {
  closeAction();
  refresh();
}
</script>

<template>
  <UButton
    v-if="props.editable"
    class="py-3"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsInquiryForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitIquiry"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="inquiries && inquiries.length">
    <div
      v-for="(item, index) in inquiries"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="6" />
      <ElementsCardDiv v-else>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Запрос о сотруднике ID #" + item["id"] }}
          </div>
        </template>
        <FormsInquiryForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :inquiry="item"
          @cancel="cancelOperation"
          @update="submitIquiry"
        />
        <div v-else>
          <ElementsLabelSlot v-if="item['info']" :label="'Информация'">{{
            item["info"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['initiator']" :label="'Иннициатор'">{{
            item["initiator"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot v-if="item['origins']" :label="'Источники'"
            >{{ item["origins"] }}
          </ElementsLabelSlot>
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
            :item="'inquiries'"
            @delete="deleteNeed(item['id'])"
            @update="
              need = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @upgrade="refresh()"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="6" />
    <p v-else class="text-red-800">Запросы о сотруднике не поступали</p>
  </div>
</template>
