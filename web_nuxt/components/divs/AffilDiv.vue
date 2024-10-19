<script setup lang="ts">
import type { Affilation } from "@/types/interfaces";

prefetchComponents(["FormsAffilationForm", "ElementsSkeletonDiv"]);

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
const affilation = ref({} as Affilation);
const affilations = ref<Affilation[]>([]);

const { refresh, status } = await useLazyAsyncData("affilations", async () => {
  affilations.value = await authFetch("/api/items/affilations/" + props.candId) as Affilation[];
});

async function submitAffilation(form: Affilation) {
  closeAction();  
  pending.value = true;
  const { message } = await authFetch(`/api/items/affilations/${props.candId}`, {
    method: "POST",
    body: form,
  }) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteAffilation(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/api/items/affilations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  await refresh();  
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
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsAffilationForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitAffilation"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="affilations && affilations.length">
    <div v-for="(item, idx) in affilations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsAffilationForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :affils="affilation"
          @cancel="cancelOperation"
          @update="submitAffilation"
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
            :navlen="3"
            @delete="deleteAffilation(item['id'])"
            @update="
              affilation = item;
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
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
