<script setup lang="ts">
import type { Education } from "@/types/interfaces";

prefetchComponents(["FormsEducationForm", "ElementsSkeletonDiv"]);

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

const collapse = ref(false);
const pending = ref(false);
const itemId = ref("");
const edit = ref(false);
const education = ref({} as Education);
const educations = ref<Education[]>([]);

const { refresh, status } = await useLazyAsyncData("educations", async () => {
  educations.value = await authFetch("/api/items/educations/" + props.candId) as Education[];
});

async function submitEducation(form: Education) {
  closeAction();
  pending.value = true;
  await emit("submit", form, "educations");
  pending.value = false;
  await refresh();
}

async function deleteEducation(id: string) {
  closeAction();
  await emit("delete", id, "educations");
  await refresh();
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
        <FormsEducationForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitEducation"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="educations && educations.length">
    <div v-for="(item, idx) in educations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsEducationForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :education="education"
          @cancel="cancelOperation"
          @update="submitEducation"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Уровень образования'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Название учебного заведения'">{{
            item["institution"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Год окончания'">{{
            item["finished"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Специальность'">{{
            item["specialty"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteEducation(item['id'])"
            @update="
              education = item;
              itemId = item['id'].toString();
              edit = true;
            "
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
