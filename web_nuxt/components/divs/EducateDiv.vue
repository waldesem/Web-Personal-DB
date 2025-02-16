<script setup lang="ts">
import type { Education } from "@/types";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const education = ref({} as Education);
const educations = ref<Education[]>([]);

const { refresh, status } = await useLazyAsyncData("educations", async () => {
  educations.value = (await authFetch(
    "/route/items/educations/" + candId.value
  )) as Education[];
});

async function submitEducation(form: Education) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/educations/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  education.value = {} as Education;
  await refresh();
  emitMessage(message);
}

async function deleteEducation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/educations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    educations.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <div v-if="editable || status == 'pending'" class="my-1">
    <UButton
      :loading="status == 'pending' || pending"
      :label="
        status == 'pending' || pending
          ? 'Обновление данных...'
          : 'Добавить запись'
      "
      variant="link"
      @click="modal = !modal"
    />
  </div>
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsEducationForm
        :education="education"
        @cancel="
          education = {} as Education;
          modal = false;
        "
        @update="submitEducation"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in educations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <DivsItemsEducateItem :item="item" />
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteEducation(item.id, idx)"
          @update="
            education = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
