<script setup lang="ts">
import type { Persons } from "@/types";

const emit = defineEmits(["update", "message"]);

const authFetch = useFetchAuth();

const props = defineProps({
  status: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
  candId: {
    type: String,
    default: "",
  },
  person: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const modal = ref(false);
const pending = ref(false);
const resume = ref({} as Persons);

async function submitResume(form: Persons) {
  pending.value = true;
  modal.value = false;
  const { message } = (await authFetch(`/route/items/persons/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  resume.value = {} as Persons;
  emit("update");
  emit("message", message);
}

async function deleteItem() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/persons/${props.candId}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  emit("message", message);
  return navigateTo("/persons");
}
</script>

<template>
  <ElementsCardDiv>
    <UModal v-model="modal" prevent-close>
      <ElementsCardDiv>
        <FormsResumeForm
          :resume="resume"
          @update="submitResume"
          @cancel="
            resume = {} as Persons;
            modal = false;
          "
        />
      </ElementsCardDiv>
    </UModal>
    <div v-if="pending || props.status === 'pending'">
      <div v-for="i in 14" :key="i" class="flex grid grid-cols-12 gap-3 mb-3">
        <div class="col-span-3">
          <USkeleton class="h-4" />
        </div>
        <div class="col-span-9">
          <USkeleton class="h-4 w-[300px]" />
        </div>
      </div>
    </div>
    <div v-else>
      <ElementsLabelSlot :label="'Фамилия'">
        {{ props.person["surname"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Имя'">
        {{ props.person["firstname"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Отчество'">
        {{ props.person["patronymic"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата рождения'">
        {{ new Date(props.person["birthday"]).toLocaleDateString("ru-RU") }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Место рождения'">
        {{ props.person["birthplace"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Гражданство'">
        {{ props.person["citizenship"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="props.person['dual']"
        :label="'Двойное гражданство'"
      >
        {{ props.person["dual"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'СНИЛС'">
        {{ props.person["snils"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'ИНН'">
        {{ props.person["inn"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Семейное положение'">
        {{ props.person["marital"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата записи'">
        {{ new Date(props.person["created"]).toLocaleString("ru-RU") }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="props.person['addition']"
        :label="'Дополнительная информация'"
      >
        {{ props.person["addition"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Материалы'">
        {{ props.person["destination"] }}
      </ElementsLabelSlot>
    </div>
    <template v-if="props.editable" #footer>
      <ElementsNaviHorizont
        :cand-id="props.candId"
        :item="'persons'"
        @delete="deleteItem"
        @update="
          resume = props.person;
          modal = true;
        "
      />
    </template>
  </ElementsCardDiv>
</template>
